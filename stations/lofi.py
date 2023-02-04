import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.commands import SlashCommandGroup
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import xml.etree.ElementTree as ET
import youtube_dl

if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"



class lofi(commands.Cog, name="Lofi Stations"):

    def __init__(self, bot):
        self.bot = bot

    lofigroup = SlashCommandGroup("lofi","Lofi Stations")

    # LofiGirl - Chill 
    @lofigroup.command(name='chill',
                    description="Lofi Girl - lofi hip hop radio - beats to relax/study to",
                    pass_context=True)
    async def lofiChill(self,ctx):

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
                video_title = info['title']
                ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
                embed=discord.Embed(title=video_title, url=video_url, description="Lofi Girl - This playlist contains the smoothest lofi hip hop beats, perfect to help you chill or study.", color=0x2ec27e)
                embed.set_thumbnail(url="https://i.imgur.com/ph10Ywa.jpg")
                await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # LofiGirl - Sleep
    @lofigroup.command(name='sleep',
                    description="Lofi Girl - lofi hip hop radio - beats to sleep/chill to",
                    pass_context=True)
    async def lofiSleep(self,ctx):

        streamURL = "https://www.youtube.com/watch?v=rUxyKA_-grg"
        
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
                video_title = info['title']
                ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
                embed=discord.Embed(title=video_title, url=video_url, description="Lofi Girl - This playlist contains the smoothest lofi hip hop beats, perfect to help you relax or fall asleep.", color=0x2ec27e)
                embed.set_thumbnail(url="https://i.imgur.com/q2n6qJT.jpg")
                await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")







# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(lofi(bot))
