import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import xml.etree.ElementTree as ET
import logging

if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"
#
# Radio Cog
#

class controls(commands.Cog, name="Controls"):


    def __init__(self, bot):
        self.bot = bot


    # Leave VC Channel
    @commands.slash_command(description="stops and disconnects the bot from voice")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.respond("Leaving Room!")

        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command:/{ctx.command} "
        logging.info(message_str)
        print(message_str)

    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(controls(bot))
