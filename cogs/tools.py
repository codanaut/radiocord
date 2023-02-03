import discord
from discord.ext import commands
import random
import aiohttp
import json
import time
#
# Tools Cog 
# 

class tools(commands.Cog, name="Random Tools Commands"):
    """TokeTimeCog"""

    def __init__(self, bot):
        self.bot = bot

    
    # List Servers
    @commands.slash_command(name='servers',
                    description="List Servers Bot is in",
                    brief="List Servers Bot is in",
                    aliases=['servers', 'serverlists'])
    async def servers(self,ctx):
        """List Server Bot is in."""
        servers = list(self.bot.guilds)
        newLine = '\n'
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")
        await ctx.respond(f"**Connected on {str(len(servers))} servers:**{newLine}{newLine.join(server.name for server in servers)}")


    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(tools(bot))