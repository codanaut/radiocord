import discord
from discord.ext import commands
import random
import aiohttp
import json
import time
import logging
#
# example Cog 
#
# Make sure to change class name in line 13 & 36
# 

class info(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot

    
    # Help
    @commands.slash_command(name='help', description="RadioCord Help")
    async def help(self,ctx):
        embed=discord.Embed(title="Welcome To RadioCord", description="Discord's Best Radio Bot", color=discord.Colour.dark_blue())
        embed.add_field(name="**How To Use**", value="----------\nYou must first be connected to a voice channel.\n\n`/station` - Any station can be started by using slash commands with the station name!\n`/leave` - Leaves the voice channel", inline=False)
        embed.add_field(name="**24/7 Mode / The Music Stopped**", value="----------\nWe do not currently support 24/7 mode and music will stop after a few hours. If your still listening and it stops just recall the station to refresh it.", inline=False)
        embed.add_field(name="**Request Stations / Report Issues**", value="----------\nYou can request new stations or report issues by visting either Github or Discord.", inline=False)
        embed.add_field(name="**GitHub**", value="----------\nYou can find out more about RadioCord by visting Github - [Github Link](https://github.com/codanaut/radiocord)", inline=False)
        embed.add_field(name="**Support Server**", value="----------\nFor any other questions or to request a station visit us on Discord! - [Discord Link](https://discord.gg/CvKeEPm49p)", inline=False)
        await ctx.respond(embed=embed)

        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command: /{ctx.command} "
        logging.info(message_str)
        print(message_str)

    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(info(bot))