import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import asyncio
import aiohttp
import xml.etree.ElementTree as ET


if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"


# Remember to change the class name!
class partyVibeRadio(commands.Cog, name="Party Vibe Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    partyVibeGroup = SlashCommandGroup("partyvibe","Party Vibe Stations")

    # Reggae Radio - https://www.partyvibe.com/reggae-radio-station/
    @partyVibeGroup.command(name='reggae',
                    description="Reggae Radio",
                    pass_context=True)
    async def partyVibeReggae(self,ctx):

        streamURL = "https://partyviberadio.com:8060"
        stationApiUrl = "http://www.partyviberadio.com:8010/stats?sid=1"
        
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSongShoutCast(ctx,stationApiUrl))
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



    # Party Vibe Radio - Rock Radio - https://www.partyvibe.com/rock-radio-station/
    @partyVibeGroup.command(name='alt-rock',
                    description="Alt Rock Radio",
                    pass_context=True)
    async def partyVibeRock(self,ctx):

        streamURL = "https://partyviberadio.com:8066"
        stationApiUrl = "http://partyviberadio.com:8032/stats?sid=1"
        
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSongShoutCast(ctx,stationApiUrl))
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



    # Party Vibe Radio - Rap Radio - https://www.partyvibe.com/rap-radio-station/
    @partyVibeGroup.command(name='rap',
                    description="Rap Radio",
                    pass_context=True)
    async def partyVibeRap(self,ctx):

        streamURL = "https://partyviberadio.com:8063"
        stationApiUrl = "http://partyviberadio.com:8032/stats?sid=1"
        
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSongShoutCast(ctx,stationApiUrl))
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



    #
    # Function to update currently playing song.
    #

    async def updateSongShoutCast(self, message, url):
        while True:
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(nowPlayingurl)
                response_text = await raw_response.text()
                root = ET.fromstring(response_text)
                nowPlaying = root.find("SONGTITLE").text
                stationURL = root.find("SERVERURL").text
                stationInfo = root.find("SERVERTITLE").text
                stationListeners = root.find("CURRENTLISTENERS").text
                stationListenersPeak = root.find("PEAKLISTENERS").text
                nowPlayingArt = "https://www.partyvibe.com/wp-content/uploads/2020/12/party-vibe-radio-logo.png"
            # Update the message with the new song information
            embed=discord.Embed(title=stationInfo, url=stationURL, color=0x2ec27e)
            embed.set_thumbnail(url=nowPlayingArt)
            embed.add_field(name="Now Playing", value=f'{nowPlaying}', inline=False)
            embed.set_footer(text=f"Current Listeners: {stationListeners} | Peak Listeners: {stationListenersPeak}")
            await message.edit(embed=embed)
            await asyncio.sleep(30)  # Wait 30 seconds before making the next request


# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(partyVibeRadio(bot))
