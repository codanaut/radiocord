import discord
from discord.ext import commands
import random
import aiohttp
import json
import time
import logging
#
# Tools Cog 
# 

class tools(commands.Cog, name="Random Tools Commands"):
    """TokeTimeCog"""

    def __init__(self, bot):
        self.bot = bot

    
    # List Servers
    @commands.slash_command(name='stats',
                    description="See Bot Stats",
                    brief="Bot Stats")
    async def stats(self,ctx):
        """List Server Bot is in."""
        servers = list(self.bot.guilds)
        newLine = '\n'
        
        fun_phrases = ["Jamming", "Blasting tunes", "Rocking out", "Playing", "Haning out"]
        fun_phrase = random.choice(fun_phrases)

        await ctx.respond(f"**{fun_phrase} on {str(len(servers))} servers**")

        # Log
        message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - User:{ctx.author} - Server:{ctx.guild} - Command: /{ctx.command} "
        logging.info(message_str)
        print(message_str)


    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(tools(bot))