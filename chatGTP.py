''' WORKING EXAMPLE '''

import discord
import asyncio

intents = discord.Intents.default()
intents.typing = True
intents.voice_states = True
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        # Join the voice channel that the controlling user is connected to
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()

        # Play the MP3 file
        vc.play(discord.FFmpegPCMAudio("./bruh.mp3", executable="C:\\ffmpeg-5.1.2-essentials_build\\bin\\ffmpeg.exe"))
        await message.channel.send("Playing bruh")
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        await vc.disconnect()

client.run('NjkzNTIzNTg4NDg5MTUwNTky.GOc3Yi.WjNvCKQzJu4ok4g50nTQ17X7H6FaIoTI2Fqvhg')
