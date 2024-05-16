import discord
from discord.ext import commands
import sys, traceback
import asyncio
import time
import logging

# set token
secret_file = open('testing.secret','r')
client_token = secret_file.readline().rstrip()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s',
    filename='bot.log',
    filemode='a' # use 'a' if you want to append only
)

intents = discord.Intents.all()


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['>?', '!!', '!?','>>']

    # Check to see if we are outside of a guild. e.g DM's etc.
    #if not message.guild:
        # Only allow ? to be used in DMs
    #    return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = [
                      'cogs.controls',
                      'cogs.tools',
                      'cogs.info',
                      'stations.paddockRadio',
                      'stations.upfm',
                      'stations.partyVibe',
                      'stations.majesticJukebox',
                      'stations.size-radio',
                      'stations.dash-country',
                      'stations.dash-rock',
                      'stations.custom-stream'
                      ]

bot = commands.Bot(command_prefix=get_prefix, description='Cheat Codes: Use at your own risk, there is no quick save irl.', intents=intents)


# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():

    if bot.auto_sync_commands:
        await bot.sync_commands()
        
    print(f'\nLogged in as: {bot.user.name}\nDiscord Version: {discord.__version__}\n-----')

    # Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
    await bot.change_presence(activity=discord.Game(name='the best tunes!'))
    
    print(f'Successfully logged in and booted...!')
    print('-----')
    servers = list(bot.guilds)
    print(f"Connected on {str(len(servers))} servers:")
    print('\n'.join(server.name for server in servers))
    print("-----")
    
    # Log
    message_str = f"{time.strftime('%m/%d/%y %I:%M%p')} - Bot Started - Connected on {str(len(servers))} servers"
    logging.info(message_str)

bot.run(client_token, reconnect=True)
