#!/bin/env python3

from disnake.ext import commands
from pytube import Playlist, YouTube
from youtubesearchpython import VideosSearch
# from time import sleep
# import threading
import disnake
import os
import asyncio
# import youtube_dl

'''
TODO add loop command
TODO add reactions to avoid spam (maybe)


BUG doesn't remove the last song from queue
BUG thinks it's in a vc when it is, in fact, not
^^ I could just check and update the boolean on every command, but that would be a lot of work

TODO refactor to use the youtube API directly instead of uisng the pytube library *pain*
^^ still need to do that but youtube doesn't like it ^^
'''

vc = 0

if os.name == "posix":
    exe = 'ffmpeg'
elif os.name == "nt":
    exe = 'C:/ffmpeg-5.1.2-essentials_build/bin/ffmpeg.exe'
## setting the cwd because I want to run the bot on startup and I'm too lazy to find the correct solution
    os.chdir("Y:\\Dropbox\\Programming\\python\\chineseGroovy")

cwd = os.getcwd()
queue = os.path.join(os.getcwd(), "queue")
hardcoded = os.path.join(cwd, "hardcodedAudio")
token = os.getenv('GROOBYTOKEN')

### create the filesystem on first boot if the ./queue directory does not exist
os.system("python3 filesystem.py")


def clearQ():
    for file in os.listdir(queue):
        if file.endswith(".mp3") or file.endswith(".mp4"):
            os.remove(os.path.join(queue, file))

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

looping = False

@bot.event
async def on_ready():
    print("bot is ready")

@bot.command() ## has the bot join the user's voice channel
async def join(ctx):
    ctx.send("-join is no longer a valid command, use -play <song name> instead")


@bot.command() ## plays bruh the same way the chatGTP code does, just with @bot instead of @client
async def bruh(ctx):
    global vc
    
    await ctx.send("moment")
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    
    vc.play(disnake.FFmpegPCMAudio(os.path.join(hardcoded, "bruh.mp3"), executable=exe))

    while vc.is_playing():
        await asyncio.sleep(1)
    vc.stop()
    await vc.disconnect()

@bot.command() ## THE ACTUAL PLAY COMMAND 23:49 1/20/23
async def play(ctx):
    global vc

    if ctx.message.guild.voice_client == None:
        ## connect to the user's voice channel
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
    else:
        vc = ctx.message.guild.voice_client


    ## if the query is megalovania because searching for megalovania isn't allowed
    if ctx.message.content.endswith("megalovania"): ## IF YOU CHANGE THE BOT PREFIX CHANGE THE HARD CODED TEXT

        if os.name == 'posix':
            os.system(f"cp {os.path.join(hardcoded, 'Megalovania.mp3')} {queue}")
        elif os.name == 'nt':
            os.system(f"copy {os.path.join(hardcoded, 'Megalovania.mp3')} {queue}")
        
        vc.play(disnake.FFmpegPCMAudio(os.path.join(queue, "Megalovania.mp3"), executable=exe))
        await asyncio.sleep(.5) ##### remove this line through #################################
        await ctx.send("no")
        await vc.disconnect()
        os.remove(os.path.join(queue, "Megalovania.mp3"))
        return ########### this line to actually have it play megalovania ################
    
        ## if the query is dsi shop theme because searching for it breaks bot
    if ctx.message.content.endswith("dsi shop theme"): ## IF YOU CHANGE THE BOT PREFIX CHANGE THE HARD CODED TEXT

        if os.name == 'posix':
            os.system(f"cp {os.path.join(hardcoded, 'Nintendo DSi Shop Theme 10 HOUR LOOP.mp3')} {queue}")
        elif os.name == 'nt':
            os.system(f"copy {os.path.join(hardcoded, 'Nintendo DSi Shop Theme 10 HOUR LOOP.mp3')} {queue}")

        vc.play(disnake.FFmpegPCMAudio(os.path.join(queue, "Nintendo DSi Shop Theme 10 HOUR LOOP.mp3"), executable=exe))
        await ctx.send("Now playing **Nintendo DSi Shop Theme 10 HORUR LOOP**")
        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(1)


    await ctx.send("Grooby:tm: is contemplating life...")
    name = ''
    if not ctx.message.content.endswith("-play"): ## if the command is followed by an argument
        argument = ctx.message.content.split(" ", 1)[1]
        if "://" in argument:
            name = getAudio(argument)

            print(name, " downloaded")

        elif "playlist" in argument: ## if the link is a playlist
            playlist = Playlist(argument)
            print(f"Number of videos in plalist: {len(playlist.video_urls)}") ################## I hope this works but it probably won't ################
            
            for i in range(len(playlist.video_urls)):
                url = playlist.video_urls[i]    

            getAudio(url)
        else:
            search = VideosSearch(argument, limit=1)

            name = getAudio(search.result()['result'][0]['link'])
    else:
        await ctx.send("actually give me a song to play")

    directory = os.listdir(queue)

    ## playing the generated mp3 file

    while directory != []:
        name = os.path.join(queue, directory[0])
        # print("name2: ", name)
        if not vc.is_playing():
            vc.play(disnake.FFmpegPCMAudio(name, executable=exe))
            await ctx.send(f"now playing **{directory[0].replace('.mp3', '')}**")
    
        while vc.is_playing() or vc.is_paused(): ## while the bot is playing audio
            await asyncio.sleep(1)
            directory = os.listdir(queue)

        try:
            if not looping:
                print(looping)
                os.remove(name) ## avoiding the bug that might be caused by the -skip command
                directory = os.listdir(queue)
            elif looping:
                print("directory[1:]", (directory[1:] + directory[0]))
                directory = directory[1:] + directory[0]
                print("new directory: ", directory)
        except:
            pass

        print("directory2: ", directory)
        
    # os.remove(name + ".mp3")
    directory = os.listdir(queue)

    vc.stop()
    await vc.disconnect() ## bot disconnects when it is done playing audio


@bot.command() ## leaves voice channel
async def leave(ctx):
    global vc

    await vc.disconnect()
    await ctx.send("left the vc")
    await asyncio.sleep(1)
    clearQ()

@bot.command() ## same as the leave
async def stop(ctx):
    global vc

    await vc.disconnect()
    await ctx.send("left the vc")
    await asyncio.sleep(1)
    clearQ()

@bot.command() ## the same as the leave command
async def begone(ctx):
    global vc

    await vc.disconnect()
    await ctx.send("left the vc")
    await asyncio.sleep(1)
    clearQ()

@bot.command() ## creator credits credits
async def credits(ctx):
    credited = True
    global vc

    await vc.connect()
    if ctx.author.voice.channel != None:
        vc.play(disnake.FFmpegPCMAudio(os.path.join(hardcoded, "credits.mp3"), executable=exe))
        
        while vc.is_playing():
            await asyncio.sleep(1)

            ## this code is horrible but idc
            if credited:
                await ctx.send("Side Character: Family Guy")
                await asyncio.sleep(5)
                await ctx.send("Emotional Support: Deaner")
                await asyncio.sleep(5)
                await ctx.send("The actual programmer: HoomBrook")
                credited = False
        vc.stop()
        await vc.disconnect()

@bot.command(name="clear", aliases=["clearQ", "clearQueue"]) ## clear queue
async def clear(ctx):
    if ctx.author.voice.channel == ctx.message.guild.voice_client:
        clearQ()
    await ctx.send("queue cleared")
    
@bot.command()
async def nowplaying(ctx):
    directory = os.listdir(queue)
    directory = [os.path.join(os.getcwd(), "queue", f) for f in directory]
    directory.sort(key=lambda x: os.path.getmtime(x))
    [i.replace(os.getcwd(), '') for i in directory]

    # await ctx.send(f"now playing **{directory[0].replace((queue + "\\"), '').replace('.mp3', '')}**")

@bot.command()
async def pause(ctx):
    global vc

    if type(vc) != None:
        try:
            vc.pause()
            await ctx.send("paused audio")
        except:
            await ctx.send("nothing to pause")
    else:
        await ctx.send("not in vc")

@bot.command()
async def resume(ctx):
    global vc

    if type(vc) != None:
        if vc.is_paused():
            vc.resume()
        else:
            await ctx.send("Nothing to resume")
    else:
        await ctx.send("not in vc")

@bot.command()
async def skip(ctx):
    global vc
    global looping

    directory = os.listdir(queue)
    directory = [os.path.join(os.getcwd(), "queue", f) for f in directory]
    directory.sort(key=lambda x: os.path.getmtime(x))

    vc.stop()
    print("skip directory: ", directory)
    if not looping:
        os.remove(os.path.join(queue, directory[0]))
    print("skip directory2: ", directory)
    await ctx.send("track skipped")

@bot.command()
async def down(ctx):
    print(ctx.message.author)
    print(ctx.message.author.id)
    if str(ctx.message.author.id) == "330520485463064597":
        print("owner detected, bot is changing status")
        await bot.change_presence(status=disnake.Status.idle, activity=disnake.Game(name="Grooby is down :("))

@bot.command()
async def up(ctx):
    print(ctx.message.author)
    print(ctx.message.author.id)
    if str(ctx.message.author.id) == "330520485463064597":
        print("owner dectected, bot is now up")
        await bot.change_presence(status=disnake.Status.online, activity=disnake.Game(name="Grooby is online!"))

@bot.command()
async def jace(ctx): ############### change 
    clearQ()
    global vc

    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()    

    if ctx.author.voice.channel != None:
        vc.play(disnake.FFmpegPCMAudio(os.path.join(hardcoded, "jace.mp3"), executable=exe))
        
        while vc.is_playing():
            await asyncio.sleep(1)

        vc.stop()
        await vc.disconnect()
    return

@bot.command()
async def github(ctx):
    await ctx.send("https://github.com/HamBrick327/Grooby")
    return

@bot.command()
async def loop(ctx):
    global looping ########### I learnded something
    looping = True
    await ctx.send("looping the queue")

@bot.command()
async def unloop(ctx):
    global looping ####### This is important and I'm an idiot
    looping = False


bot.run(token)