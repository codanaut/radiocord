import discord
from discord.embeds import Embed
from discord.ext import commands
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
class dashCountryRadio(commands.Cog, name="Dash Country Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    
    # DashVille
    @commands.slash_command(name='dashville',
                    description="Dashville - Country Hits 2000-2020",
                    pass_context=True)
    async def dashVille(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH82"
        stationApiUrl = "https://streamdb7web.securenetsystems.net/player_status_update/DASH82.xml"
        stationUrl = "https://dashradio.com/dashville"
        stationArt = "https://dashradio-files.s3.amazonaws.com/development/icon_logos/232/logos/7c41cee5-c194-4d0b-aa51-ebf20b590e03.png"
        stationTitle = "DashVille"
        stationDescription = "Country hits 2000-2020"

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
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # Hooche Country
    @commands.slash_command(name='hoochecountry',
                    description="Hooche Country - Mainstream Hits",
                    pass_context=True)
    async def hoocheCountry(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH15"
        stationApiUrl = "https://streamdb5web.securenetsystems.net/player_status_update/DASH15.xml"
        stationUrl = "https://dashradio.com/hoochecountry"
        stationArt = "https://dashradio-files.s3.amazonaws.com/development/icon_logos/226/logos/404ac8e5-9a9a-46ac-8c2a-40d9ab808a42.png"
        stationTitle = "Hooche Country"
        stationDescription = "Hooche Country - Mainstream Hits"

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
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



    # The Ranch
    @commands.slash_command(name='theranch',
                    description="The Ranch - Classic Country",
                    pass_context=True)
    async def theRanch(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH13"
        stationApiUrl = "https://streamdb5web.securenetsystems.net/player_status_update/DASH13.xml"
        stationUrl = "https://dashradio.com/TheRanch"
        stationArt = "https://s3.amazonaws.com/dashradio-files/now_playing_artwork/TheRanch.jpg"
        stationTitle = "The Ranch - Classic Country"
        stationDescription = "This is country music, before they made it into pop. It dont mean a thang, if it aint got that twang."

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
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



    # Dash Country X
    @commands.slash_command(name='dashcountry',
                    description="Dash Country - country music's biggest hits",
                    pass_context=True)
    async def dashcountryx(self,ctx):

        streamURL = "https://ice55.securenetsystems.net/DASH35"
        stationApiUrl = "https://streamdb5web.securenetsystems.net/player_status_update/DASH35.xml"
        stationUrl = "https://dashradio.com/CountryX"
        stationArt = "https://dashradio-files.s3.amazonaws.com/development/icon_logos/43/logos/17666691-1291-4127-98b4-7cd4511445bc.png"
        stationTitle = "Dash Country"
        stationDescription = "The home for country music's biggest hits and upcoming superstars."

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
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


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
   bot.add_cog(dashCountryRadio(bot))
