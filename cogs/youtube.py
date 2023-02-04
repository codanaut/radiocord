import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import xml.etree.ElementTree as ET
import youtube_dl

if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"

class youtube(commands.Cog, name="Youtube Commands"):

    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    
    # youtube
    @commands.slash_command(name='youtube',
                    description="Youtube Link",
                    pass_context=True)
    async def youtube(self,ctx, *, url: str):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting!")
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
                info = ydl.extract_info(url, download=False)
                video_url = info['url']
                video_title = info['title']
                video_id = info['id']
                video_thumbnail = f"https://i3.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                video_description = info['description']
                ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))
                embed=discord.Embed(title=video_title, url=video_url, description=video_description, color=0x2ec27e)
                embed.set_thumbnail(url=video_thumbnail)
                await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(youtube(bot))
