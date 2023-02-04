import discord
from discord.embeds import Embed
from discord.ext import commands
import random
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import asyncio
import aiohttp
import json
import xml.etree.ElementTree as ET
import youtube_dl

if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"
#
# Radio Cog
#

class radio(commands.Cog, name="Radio Commands"):
    """RadioCog"""

    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    # Paddock Radio - https://www.paddockradio.net/
    @commands.slash_command(name='paddockradio',
                    description="Paddock Radio",
                    pass_context=True)
    async def paddockradio(self,ctx):

        streamURL = "http://stream.paddockradio.net/radio/8000/radio.mp3"
        stationApiUrl = "https://stream.paddockradio.net/api/nowplaying"
        
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


    # OJRock - https://radio.mpaq.org/
    @commands.slash_command(name='rock',
                    description="OJRock Radio",
                    pass_context=True)
    async def rock(self,ctx):
        source = FFmpegPCMAudio("http://mpaq.org:5804/rock.mp3", executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            await ctx.respond(f"Connecting to {connected.channel}")
            await ctx.edit(content='Now Playing: OJRock Radio - https://radio.mpaq.org/')
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    
    # Reggae Radio - https://www.partyvibe.com/reggae-radio-station/
    @commands.slash_command(name='reggae',
                    description="Reggae Radio",
                    pass_context=True)
    async def reggae(self,ctx):

        streamURL = "https://partyviberadio.com:8060"
        stationApiUrl = "http://www.partyviberadio.com:8010/stats?sid=1"
        
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
            self.updateTask = asyncio.create_task(self.updateSongShoutCast(ctx,stationApiUrl))
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # LofiGirl
    @commands.slash_command(name='lofigirl',
                    description="Lofi Radio",
                    pass_context=True)
    async def lofigirl(self,ctx):

        streamURL = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
        
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!")
            await ctx.respond(embed=connectionEmbed)
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet' : 'true',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(streamURL, download=False)
                video_url = info['url']
                ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
                embed=discord.Embed(title="Lofi Girl", url=video_url, description="Lofi Music", color=0x2ec27e)
                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/2/23/Lofi_girl_logo.jpg")
                await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # youtube
    @commands.slash_command(name='youtube',
                    description="Youtube Link",
                    pass_context=True)
    async def youtube(self,ctx, *, stream_url: str):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!")
            await ctx.respond(embed=connectionEmbed)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(stream_url, download=False)
                video_url = info['url']
                video_title = info['title']
                ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
                embed=discord.Embed(title=video_title, url=video_url, color=0x2ec27e)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/174/174883.png")
                await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")




    #
    # Functions to update currently playing songs depending on radio server. 
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
                nowPlayingArt = "https://cdn-icons-png.flaticon.com/512/2226/2226904.png"
            # Update the message with the new song information
            embed=discord.Embed(title=stationInfo, url=stationURL, color=0x2ec27e)
            embed.set_thumbnail(url=nowPlayingArt)
            embed.add_field(name="Now Playing", value=f'{nowPlaying}', inline=False)
            await message.edit(embed=embed)
            await asyncio.sleep(30)  # Wait 30 seconds before making the next request

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(radio(bot))
