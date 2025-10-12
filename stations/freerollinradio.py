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
            voice_client = await connected.channel.connect()
            voice_client.play(source, after=None)
            
            connectionEmbed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment! Hang Tight!")
            connectionEmbed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=connectionEmbed)
            
            if self.updateTask is not None:
                self.updateTask.cancel()
                
            self.updateTask = asyncio.create_task(self.updateSongiceCast(ctx, stationApiUrl))
        else:
            await ctx.respond('Please connect to a voice channel')
            
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")

    async def updateSongiceCast(self, message, url):
        while True:
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:
                try:
                    raw_response = await session.get(nowPlayingurl)
                    response = await raw_response.text()
                    data = json.loads(response)
                    
                    source_info = data.get('icestats', {}).get('source')
                    if not source_info:
                        print("Source data not found in API response.")
                        await asyncio.sleep(30)
                        continue

                    # FIX: Check if source_info is a list and grab the first element if it is.
                    if isinstance(source_info, list):
                        source_data = source_info[0]
                    else:
                        source_data = source_info

                    #stationName = source_data.get('server_name', 'Unknown Station')
                    stationName = "Free Rollin Radio"
                    stationURL = source_data.get('server_url', '')
                    #stationDescription = source_data.get('server_description', '')
                    stationDescription = "Playing the best tunes!"
                    nowPlaying = source_data.get('title', 'Unknown Title')
                    stationListeners = source_data.get('listeners', 0)
                    stationListenersPeak = source_data.get('listener_peak', 0)
                    
                    embed = discord.Embed(title=stationName, url=stationURL, description=stationDescription, color=0x2ec27e)
                    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7674/7674917.png")
                    embed.add_field(name="Now Playing", value=f'{nowPlaying}', inline=False)
                    embed.set_footer(text=f"Current Listeners: {stationListeners} | Peak Listeners: {stationListenersPeak}")
                    
                    await message.edit(embed=embed)

                except Exception as e:
                    print(f"An error occurred while updating the song: {e}")

            await asyncio.sleep(30)

def setup(bot):
   bot.add_cog(freerollinradio(bot))