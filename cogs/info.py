import discord
from discord.ext import commands
import random
import aiohttp
import json
import time

#
# example Cog 
#
# Make sure to change class name in line 13 & 36
# 

class info(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot

    
    # List Servers
    @commands.slash_command(name='help', description="lists commands")
    async def help(self,ctx):
        embed=discord.Embed(title="Help", description="Bot Commands", color=discord.Colour.dark_blue())
        embed.add_field(name="**Crypto**", value="----------\n`/eth` - Get eth price\n`/btc` - get btc price\n`/nano` - Get the nano price\n", inline=False)
        embed.add_field(name="**Fun**", value="----------\n`/8ball` - 8ball answers all!\n`/repeat` - repeat your input\n`/bored` - Suggest something to do\n`/joke` - A random joke\n`toke` - Its time to toke\n`gif`- Random toking gif", inline=False)
        embed.add_field(name="**xkcd**", value="----------\n`/xkcd` - Get the newest xkcd\n`/randomxkcd` - Get a random xkcd", inline=False)
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")
        await ctx.respond(embed=embed)

    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.

def setup(bot):
   bot.add_cog(info(bot))