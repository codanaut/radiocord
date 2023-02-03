import discord
from discord.embeds import Embed
from discord.ext import commands
import random
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer

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

    # Paddock Radio - https://www.paddockradio.net/
    @commands.slash_command(name='paddockradio',
                    description="Paddock Radio",
                    pass_context=True)
    async def paddockradio(self,ctx):
        source = FFmpegPCMAudio("http://stream.paddockradio.net/radio/8000/radio.mp3", executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            await ctx.respond(f"Connecting to {connected.channel}")
            await ctx.edit(content='Now Playing: Paddock Radio - https://www.paddockradio.net/')
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # UPFM - https://upfm.co.nz/
    @commands.slash_command(name='upfm',
                    description="UPFM Radio",
                    pass_context=True)
    async def upfm(self,ctx):
        source = FFmpegPCMAudio("https://stream.upfm.live/radio/8000/radio.mp3", executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            await ctx.respond(f"Connecting to {connected.channel}")
            await ctx.edit(content='Now Playing: UPFM Radio - https://upfm.co.nz/')
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
        source = FFmpegPCMAudio("https://partyviberadio.com:8060", executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            await ctx.respond(f"Connecting to {connected.channel}")
            await ctx.edit(content='Now Playing: Reggae Radio - https://www.partyvibe.com/reggae-radio-station/')
        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    # Leave VC Channel
    @commands.slash_command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx):
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")
        await ctx.voice_client.disconnect()
        await ctx.respond("Leaving Room!")


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(radio(bot))
