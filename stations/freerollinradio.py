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

    # FreeRollinRadio - https://www.paddockradio.net/
    @commands.slash_command(name='freerollinradio', description="Free Rollin Radio")
    async def freerollinradio(self, ctx):
        
        # AzuraCast URLs
        streamURL = "https://radio.codanaut.com/listen/free_rollin_radio/radio.mp3"
        stationApiUrl = "https://radio.codanaut.com/api/nowplaying"
        
        # Setup Source
        # Note: Added options to ignore SSL errors for FFmpeg if using raw IP with HTTPS
        source = FFmpegPCMAudio(streamURL, executable=ffmpegPath, options='-vn')

        # Handle Voice Connection
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            
        connected = ctx.author.voice
        if connected:
            # 1. Defer the interaction immediately
            await ctx.defer()

            # 2. Connect to voice
            voice_client = await connected.channel.connect()
            voice_client.play(source, after=None)
            
            # 3. Create the initial Embed (Just like your working fix)
            initial_embed = Embed(title="Free Rollin Radio", color=0x2ec27e, description="Connecting to AzuraCast Stream...")
            initial_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/7674/7674917.png")
            initial_embed.add_field(name="Now Playing", value="*Fetching info...*", inline=False)
            initial_embed.set_footer(text="Station: Free Rollin Joint")

            # 4. Send the message and CAPTURE the message object
            # We use ctx.send or ctx.respond depending on your library version, 
            # but ctx.send is usually safer for followups after defer().
            now_playing_message = await ctx.respond(embed=initial_embed)
            
            # If using Pycord, ctx.respond returns an Interaction, so we might need to fetch the message:
            if not isinstance(now_playing_message, discord.Message):
                 now_playing_message = await now_playing_message.original_response()

            # 5. Cancel old tasks
            if self.updateTask is not None:
                self.updateTask.cancel()
            
            # 6. Start the background task passing the SPECIFIC MESSAGE
            self.updateTask = asyncio.create_task(self.updateSongAzuraCast(now_playing_message, stationApiUrl))
            
            # Log it
            print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")

        else:
            await ctx.respond('Please Connect to voice channel', ephemeral=True)


    async def updateSongAzuraCast(self, message_to_edit, url):
        # We start the loop immediately. 
        # (Optional) You can leave a tiny 1-second buffer just to be safe, but 10 was too long.
        await asyncio.sleep(1) 
        
        while True:
            nowPlayingurl = url
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(nowPlayingurl, ssl=False) as raw_response:
                        response_text = await raw_response.text()
                        data = json.loads(response_text)

                        if isinstance(data, list) and len(data) > 0:
                            station_data = data[0]
                        elif isinstance(data, dict):
                            station_data = data
                        else:
                            print("Unknown API response format")
                            # If we fail to read data, wait a bit and try again
                            await asyncio.sleep(30)
                            continue

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

                        embed = discord.Embed(title=stationName, url=stationURL, description=stationDescription, color=0x2ec27e)
                        if trackArt:
                            embed.set_thumbnail(url=trackArt)
                        
                        embed.add_field(name="Now Playing", value=f'🎵 {trackTitle}\n👤 {trackArtist}', inline=False)
                        embed.set_footer(text=f"Listeners: {listeners}")

                        await message_to_edit.edit(embed=embed)

                except discord.errors.NotFound:
                    print("Message deleted, stopping updater.")
                    break
                except Exception as e:
                    print(f"Error in AzuraCast update: {e}")
            
            # This is the important change:
            # We sleep AFTER the update is done, so the first one happens instantly.
            await asyncio.sleep(30)

def setup(bot):
   bot.add_cog(freerollinradio(bot))