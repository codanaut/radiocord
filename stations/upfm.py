import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import asyncio
import aiohttp
import json
import xml.etree.ElementTree as ET


if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"


# Remember to change the class name!
class upfmRadio(commands.Cog, name="UPFM Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    # UPFM - https://upfm.co.nz/
    @commands.slash_command(name='upfm',
                    description="UPFM Radio",
                    pass_context=True)
    async def upfm(self,ctx):

        streamURL = "https://stream.upfm.live/radio/8000/radio.mp3"
        stationApiUrl = "https://stream.upfm.live/api/nowplaying"

        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel}")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSongAzuraCast(ctx,stationApiUrl))
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")        



    #
    # Function to update currently playing song. 
    #

    async def updateSongAzuraCast(self, message, url):
        while True:
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(nowPlayingurl)
                response = await raw_response.text()
                response = json.loads(response)
                stationInfo = response[0]['station']['name']
                stationURL = response[0]['station']['url']
                stationDescription = response[0]['station']['description']
                nowPlaying = response[0]['now_playing']['song']['title']
                nowPlayingArtist = response[0]['now_playing']['song']['artist']
                nowPlayingArt = response[0]['now_playing']['song']['art']
            # Update the message with the new song information
            embed=discord.Embed(title=stationInfo, url=stationURL, description=stationDescription, color=0x2ec27e)
            embed.set_thumbnail(url=nowPlayingArt)
            embed.add_field(name="Now Playing", value=f'{nowPlaying} \n {nowPlayingArtist}', inline=False)
            await message.edit(embed=embed)
            await asyncio.sleep(30)  # Wait 30 seconds before making the next request



# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(upfmRadio(bot))
