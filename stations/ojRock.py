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


# Remember to change the class name and the name=!
class ojRockRadio(commands.Cog, name="OJ Rock Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None


    # OJRock - https://radio.mpaq.org/
    @commands.slash_command(name='ojrockradio',
                    description="OJRock Radio",
                    pass_context=True)
    async def ojrockradio(self,ctx):
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



# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(ojRockRadio(bot))
