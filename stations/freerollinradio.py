import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio
import asyncio
import aiohttp
import json

if os.name == 'nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"

class freerollinradio(commands.Cog, name="FreeRollinRadio"):

    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None

    @commands.slash_command(name='freerollinradio', description="Free Rollin Radio")
    async def freerollinradio(self, ctx):
        streamURL = "http://100.108.204.69:20420/radio.mp3"
        stationApiUrl = "http://100.108.204.69:20420/status-json.xsl"
        
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath)
        
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            
        connected = ctx.author.voice
        if connected:
            await ctx.defer()

            voice_client = await connected.channel.connect()
            voice_client.play(source, after=None)
            
            # Create the initial embed for the PUBLIC "Now Playing" message.
            initial_embed = Embed(title="Free Rollin Radio", color=0x2ec27e, description="Playing the best tunes!")
            initial_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7674/7674917.png")
            initial_embed.add_field(name="Now Playing", value="*Fetching info...*", inline=False)
            initial_embed.set_footer(text="Listeners: N/A | Peak: N/A")

            # Send the public message that everyone can see and we can update forever.
            now_playing_message = await ctx.send(embed=initial_embed)
            
            # Cancel any old update task that might be running.
            if self.updateTask is not None:
                self.updateTask.cancel()
                
            # Start the background task to update the public message.
            self.updateTask = asyncio.create_task(self.updateSongiceCast(now_playing_message, stationApiUrl))

            # Edit our private "thinking..." message into a final confirmation for the user.
            await ctx.edit(content=f"✅ Started streaming in **{connected.channel.name}**!")

        else:
            # Send a private message if the user isn't in a voice channel.
            await ctx.respond('Please connect to a voice channel', ephemeral=True)
            
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")

    async def updateSongiceCast(self, message_to_edit, url):
        while True:
            await asyncio.sleep(30) # Wait first to avoid hitting the API too quickly at startup
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:
                try:
                    raw_response = await session.get(nowPlayingurl)
                    response = await raw_response.text()
                    data = json.loads(response)
                    
                    source_info = data.get('icestats', {}).get('source')
                    if not source_info:
                        print("Source data not found in API response.")
                        continue

                    if isinstance(source_info, list):
                        source_data = source_info[0]
                    else:
                        source_data = source_info

                    stationName = "Free Rollin Radio"
                    stationURL = source_data.get('server_url', '')
                    stationDescription = "Playing the best tunes!"
                    nowPlaying = source_data.get('title', 'Unknown Title')
                    stationListeners = source_data.get('listeners', 0)
                    stationListenersPeak = source_data.get('listener_peak', 0)
                    
                    embed = discord.Embed(title=stationName, url=stationURL, description=stationDescription, color=0x2ec27e)
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7674/7674917.png")
                    embed.add_field(name="Now Playing", value=f'🎵 {nowPlaying}', inline=False)
                    embed.set_footer(text=f"Listeners: {stationListeners} | Peak: {stationListenersPeak}")
                    
                    await message_to_edit.edit(embed=embed)

                except discord.errors.NotFound:
                    print("Update message not found. Stopping task.")
                    break # Stop the loop if the message was deleted
                except Exception as e:
                    print(f"An error occurred while updating the song: {e}")


def setup(bot):
   bot.add_cog(freerollinradio(bot))