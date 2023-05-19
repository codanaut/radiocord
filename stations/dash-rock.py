import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import logging

if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"


# Remember to change the class name!
class dashRockRadio(commands.Cog, name="Dash Rock Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    
    # Dash Rock
    @commands.slash_command(name='dashrock',
                    description="Dash Rock - All your favorite rock music, all in one place!",
                    pass_context=True)
    async def dashRock(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH38"
        stationApiUrl = "https://streamdb5web.securenetsystems.net/player_status_update/DASH38.xml"
        stationUrl = "https://dashradio.com/dashrockx"
        stationArt = "https://dashradio-files.s3.amazonaws.com/development/icon_logos/22/logos/a4d80dbb-f403-4dcf-8302-97c8dda45bbc.png"
        stationTitle = "Dash Rock"
        stationDescription = "All your favorite rock music, all in one place!"

        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment! Hang Tight!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSong(ctx,stationApiUrl,stationTitle,stationUrl,stationArt,stationDescription))
        else:
            await ctx.respond('Plase Connect to voice channel')
        
        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command:/{ctx.command} "
        logging.info(message_str)
        print(message_str)


    # Dash Alt
    @commands.slash_command(name='dashalt',
                    description="Dash Alt - Top Alternative Hits",
                    pass_context=True)
    async def dashalt(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH12"
        stationApiUrl = "https://streamdb5web.securenetsystems.net/player_status_update/DASH12.xml"
        stationUrl = "https://dashradio.com/altx"
        stationArt = "https://dashradio-files.s3.amazonaws.com/icon_logos/DASHXALT/dash_x_alt_nowplaying_1080.jpg"
        stationTitle = "Dash Alt"
        stationDescription = "Catch top alternative hits by the bands you love! "

        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment! Hang Tight!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSong(ctx,stationApiUrl,stationTitle,stationUrl,stationArt,stationDescription))
        else:
            await ctx.respond('Plase Connect to voice channel')
        
        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command:/{ctx.command} "
        logging.info(message_str)
        print(message_str)



    # Dash Alt Classics
    @commands.slash_command(name='dashaltclassics',
                    description="Dash Alt Classics - Yesterday's Alternative Hits!",
                    pass_context=True)
    async def dashaltclassics(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH83"
        stationApiUrl = "https://streamdb7web.securenetsystems.net/player_status_update/DASH83.xml"
        stationUrl = "https://dashradio.com/altclassics"
        stationArt = "https://dashradio-files.s3.amazonaws.com/development/icon_logos/206/logos/44d18a0f-f5c7-4dfc-84a0-0d231775bf3a.png"
        stationTitle = "Dash Alt Classics"
        stationDescription = "Yesterday's Alternative Hits!"

        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment! Hang Tight!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            if self.updateTask is not None:
                self.updateTask.cancel()
            self.updateTask = asyncio.create_task(self.updateSong(ctx,stationApiUrl,stationTitle,stationUrl,stationArt,stationDescription))
        else:
            await ctx.respond('Plase Connect to voice channel')
        
        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command:/{ctx.command} "
        logging.info(message_str)
        print(message_str)






    #
    # Function to update currently playing song.
    #

    async def updateSong(self, message, url, stationTitle, stationUrl,stationArt,stationdescription):
        while True:
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:  # Async HTTP request
                raw_response = await session.get(nowPlayingurl)
                response_text = await raw_response.text()
                root = ET.fromstring(response_text)
                nowPlaying = root.find("title").text
                nowPlayingArtist = root.find("artist").text
                nowPlayingArt = stationArt
                stationURL = stationUrl
                stationInfo = stationTitle
                stationDescription = stationdescription
            # Update the message with the new song information
            embed=discord.Embed(title=stationInfo, url=stationURL, description=stationDescription, color=0x2ec27e)
            embed.set_thumbnail(url=nowPlayingArt)
            embed.add_field(name="Now Playing", value=f'{nowPlaying} \n {nowPlayingArtist}', inline=False)
            await message.edit(embed=embed)
            await asyncio.sleep(30)  # Wait 30 seconds before making the next request


# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(dashRockRadio(bot))
