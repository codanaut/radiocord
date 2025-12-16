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
        
        # --- CONFIGURATION ---
        streamURL = "https://radio.codanaut.com/listen/free_rollin_joint/radio.mp3"
        stationApiUrl = "https://radio.codanaut.com/api/nowplaying"
        
        # --- VOICE CONNECTION ---
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            
        connected = ctx.author.voice
        if not connected:
            await ctx.respond('Please connect to a voice channel', ephemeral=True)
            return

        # 1. Defer the interaction immediately so we don't time out
        await ctx.defer()

        # 2. Connect and Play
        voice_client = await connected.channel.connect()
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath, options='-vn')
        voice_client.play(source, after=None)
        
        # 3. Create the initial Embed
        initial_embed = Embed(title="Free Rollin Radio", color=0x2ec27e, description="Connecting to AzuraCast Stream...")
        initial_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7674/7674917.png")
        initial_embed.add_field(name="Now Playing", value="*Fetching info...*", inline=False)
        initial_embed.set_footer(text="Station: Free Rollin Joint")

        # 4. Send a FRESH message dedicated to the "Now Playing" display
        # We use ctx.channel.send to ensure we get a pure Message object, independent of the interaction webhook
        now_playing_message = await ctx.channel.send(embed=initial_embed)
        
        # 5. Cancel old tasks
        if self.updateTask is not None:
            self.updateTask.cancel()
            
        # 6. Start the background task passing the SPECIFIC MESSAGE
        self.updateTask = asyncio.create_task(self.updateSongAzuraCast(now_playing_message, stationApiUrl))
        
        # 7. Update the original interaction to say "Done" (Just like your Icecast script)
        await ctx.followup.send(f"✅ Started streaming in **{connected.channel.name}**!", ephemeral=True)
        
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")


    async def updateSongAzuraCast(self, message_to_edit, url):
        # Initial short sleep to let the message register
        await asyncio.sleep(1)
        
        while True:
            # Add timeout so the loop doesn't freeze if the API hangs
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    # ssl=False for IP-based HTTPS
                    async with session.get(url, ssl=False) as raw_response:
                        response_text = await raw_response.text()
                        data = json.loads(response_text)

                        # Handle List vs Dict response
                        if isinstance(data, list) and len(data) > 0:
                            station_data = data[0]
                        elif isinstance(data, dict):
                            station_data = data
                        else:
                            print("Unknown API response format")
                            continue

                        # Extract Data
                        station_info = station_data.get('station', {})
                        now_playing_info = station_data.get('now_playing', {})
                        song_info = now_playing_info.get('song', {})

                        stationName = station_info.get('name', 'Free Rollin Radio')
                        stationURL = station_info.get('url', '')
                        stationDescription = station_info.get('description', 'Streaming Live')
                        
                        trackTitle = song_info.get('title', 'Unknown Title')
                        trackArtist = song_info.get('artist', 'Unknown Artist')
                        trackArt = song_info.get('art', '')

                        listeners = station_data.get('listeners', {}).get('current', 0)

                        # Build Embed
                        embed = discord.Embed(title=stationName, url=stationURL, description=stationDescription, color=0x2ec27e)
                        if trackArt:
                            embed.set_thumbnail(url=trackArt)
                        
                        embed.add_field(name="Now Playing", value=f'🎵 {trackTitle}\n👤 {trackArtist}', inline=False)
                        embed.set_footer(text=f"Listeners: {listeners}")

                        # Edit the specific message
                        await message_to_edit.edit(embed=embed)

                except asyncio.TimeoutError:
                    print("Update timed out. Skipping.")
                except discord.errors.NotFound:
                    print("Message deleted, stopping updater.")
                    break
                except Exception as e:
                    print(f"Error in AzuraCast update: {e}")
            
            # Sleep at the END of the loop so the first update is fast
            await asyncio.sleep(30)

def setup(bot):
   bot.add_cog(freerollinradio(bot))