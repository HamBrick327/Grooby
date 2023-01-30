from disnake.ext import commands
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
from time import sleep
# import threading
import disnake
import os
import asyncio
# import youtube_dl

'''
TODO add slash commands: no one actually cares about slash commands, adding them is placed on hold at best
TODO add search command // jesus I had to retype funciton three times
TODO add queue
TODO add pause/resume, maybe with nested bot events
TODO add loop command

BUG thinks it's in a vc when it is, in fact, not
BUG refuses to play megalovania
BUG repeats last song in queue? need to test more to recreate it
'''

global vc
global voice_channel
global name


cwd = os.getcwd()
queue = os.getcwd() + "\\queue"
connected = False

# def goBot():
#     bot.run("NjkzNTIzNTg4NDg5MTUwNTky.GOc3Yi.WjNvCKQzJu4ok4g50nTQ17X7H6FaIoTI2Fqvhg")

# def checkQ():
#     print(os.listdir("./queue"))
#     sleep(1)

def clearQ():
    for file in os.listdir(queue):
        if file.endswith(".mp3") or file.endswith(".mp4"):
            os.remove(queue + "\\" + file)

def getAudio(url):
    ## doing it the pytube way
    video = YouTube(url)
    audio = video.streams.filter(only_audio=True).first() ## download only the video's audio, but still as a mp4 file
    output = audio.download(output_path=queue) ## set the output destination

    ## change the file extension, ooga booga style
    name, ext = os.path.splitext(output)
    ext = '.mp3'
    os.rename(output, (name + ext))
    return name

## bot settings
command_sync_flags = commands.CommandSyncFlags.none()
command_sync_flags.sync_commands = False
intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True
intents.voice_states = True


bot = commands.Bot(
    command_prefix='-',
    command_sync_flags=command_sync_flags,
    intents=intents
)

# @bot.slash_command(description="Plays the test file in the user's current vc")
# async def bruh(inter, user: disnake.User):
    # print(user)
    # await inter.respnse.send_message("gamer")

@bot.event
async def on_ready():
    print("bot is ready")

@bot.command() ## has the bot join the user's voice channel
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()


@bot.command() ## plays bruh the same way the chatGTP code does, just with @bot instead of @client
async def bruh(ctx):
    await ctx.send("moment")
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    
    # vc.play(disnake.FFmpegPCMAudio("./bruh.mp3", executable="C:/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe")) ## remove the executables argument when running on linux, windows 10 wouldn't let me add the sytem enviornemt variable
    vc.play(disnake.FFmpegPCMAudio("./bruh.mp3", executable="C:/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe"))

    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
    await vc.disconnect()

@bot.command() ## THE ACTUAL PLAY COMMAND 23:49 1/20
async def play(ctx):


    if ctx.message.guild.voice_client == None:
        ## connect to the user's voice channel
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
    else:
        vc = ctx.message.guild.voice_client


    ## if the query is megalovania because searching for megalovania isn't allowed
    if ctx.message.content.endswith("megalovania"): ## IF YOU CHANGE THE BOT PREFIX CHANGE THE HARD CODED TEXT
        await asyncio.sleep(1.5)
        await ctx.send("no")
        await vc.disconnect()
        return

    await ctx.send("Grooby:tm: is contemplating life...")
    name = ''
    if not ctx.message.content.endswith(";;play"): ## if the command is followed by an argument
        argument = ctx.message.content.split(" ", 1)[1]
        if "://" in argument:
            name = getAudio(argument)

            print(name, " downloaded")
        else:
            search = VideosSearch(argument, limit=1)

            name = getAudio(search.result()['result'][0]['link'])

    directory = os.listdir(queue)

    ## playing the generated mp3 file
    print(queue, directory[0])
    print(name)

    while directory != []:
        name = queue + "\\" + directory[0]
        vc.play(disnake.FFmpegPCMAudio(name, executable="C:/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe"))
    
        await asyncio.sleep(5)
        while vc.is_playing(): ## while the bot is playing audio
            await asyncio.sleep(1)
            directory = os.listdir(queue)

        os.remove(name)
        directory = os.listdir(queue)
        
    # os.remove(name + ".mp3")
    # directory = os.listdir(queue)
    vc.stop()
    await vc.disconnect() ## bot disconnects when it is done playing audio


@bot.command() ## leaves voice channel
async def leave(ctx):
    vc = ctx.message.guild.voice_client
    await vc.disconnect()
    clearQ()
    await ctx.send("left the vc")


@bot.command() ## end credits
async def credits(ctx):
    credited = True

    if ctx.author.voice.channel != None:
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(disnake.FFmpegPCMAudio(cwd + "\\credits.mp3", executable="C:/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe"))
        
        while vc.is_playing():
            await asyncio.sleep(1)

            ## this code is horrible but idc
            if credited:
                await ctx.send("Side Character: Family Guy")
                await asyncio.sleep(5)
                await ctx.send("Emotional Support: Deaner")
                await asyncio.sleep(5)
                await ctx.send("Main Developer: HoomBrook")
                credited = False
        vc.stop()
        await vc.disconnect()

@bot.command() ## clear queue
async def clear(ctx):
    if ctx.author.voice.channel == ctx.message.guild.voice_client:
        clearQ()
    await ctx.send("queue cleared @", ctx.author.username)

bot.run('<your token here>')
