import discord
from discord.embeds import Embed
from discord.ext import commands
import time
import os
from discord import FFmpegPCMAudio, PCMVolumeTransformer

import xml.etree.ElementTree as ET


if os.name =='nt':
    ffmpegPath = r"C:\\FFmpeg\\bin\\ffmpeg.exe"
else:
    ffmpegPath = "ffmpeg"


# Remember to change the class name and the name=!
class ojRockRadio(commands.Cog, name="OJ Rock Radio"):


    def __init__(self, bot):
        self.bot = bot
        self.updateTask = None


    # OJRock - https://radio.mpaq.org/
    @commands.slash_command(name='ojrockradio',
                    description="OJRock Radio",
                    pass_context=True)
    async def ojrockradio(self,ctx):
        source = FFmpegPCMAudio("http://mpaq.org:5804/rock.mp3", executable=ffmpegPath)
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        connected = ctx.author.voice
        if connected:
            await connected.channel.connect()
            ctx.voice_client.play(source, after=None)
            embed = Embed(title=f"Connecting to {connected.channel} and starting stream!", description="This may take a moment!")
            embed.set_footer(text="(note: some live streams may go offline at times, if a stream is dead try another)")
            await ctx.respond(embed=embed)

            # Set the station Info
            embed = Embed(title="OJ Rock", description="Occupy Journey Classic Rock", url="https://radio.mpaq.org/")
            #embed.add_field(name="Now Playing", value="Song Playing", inline=False)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2226/2226904.png")
            #embed.set_footer(text="Some footer note about the station")
            await ctx.edit(embed=embed)

        else:
            await ctx.respond('Plase Connect to voice channel')
        print(f"{time.strftime('%m/%d/%y %I:%M%p')} - /{ctx.command} - Server:{ctx.guild} - User:{ctx.author}")



# Remember we give bot.add_cog() the name of the class you set at the top.
def setup(bot):
   bot.add_cog(ojRockRadio(bot))
