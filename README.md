# Grooby
Not groovy discord bot.... Grooby

I don't run this bot myself on windows very much, so most of the features and startup things aren't tested or really intended for windows. YMMV

If you have python all installed and setup, this should be pretty easy to just get going assuming you know how to set up a bot in the discord dev portal.

Use python3 -m pip install -r requirements.txt to install dependencies

The filesystem.py script should run automatically on first boot, if there is not a ./queue directory then run it manually.

# mf-dl is not mine, find it at *https://gitgud.io/Pyxia/mf-dl.git* was very useful to me and getting around the github file size limit

I am aware this bot uses a library that is no longer being supported

This bot plays youtube videos based on the text given in the -play command, and it can use playlist links or direct links aswell.

This bot is quite scuffed and breaks at some of the weirdest times.

This bot downloads music and adds it to the ./queue directory, which is not part of this repo

main.py assumes you have python3 set as a system path for running your python executable, if it isn't adjust accordingly because I am lazy and don't want to have to detect the python installation for every computer. That and you probably wouldn't want me automatically looking through your system files.

I had a bug where the mediafire link might've expired or became otherwise unusable, might be fixed, might be something I have to fix in the futute for anyone who wants to host this scuffed bot themselves instead of any of the actual good ones

### in the pytube library installation change line 30 of cipher.py from `var_regex = re.compile(r"^\w+\W")` to `var_regex = re.compile(r"^\$*\w+\W")` as per [this stackoverflow post](https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w) and [this github issue](https://github.com/pytube/pytube/issues/1199) this fixes the random bug that I was getting every once in a while

## testing changes is for losers


  -play <song to play>

  -leave
    -begone
    -stop
    -leave

  -clear

  -queue (lists the songs in the queue)

  -up
  -down (these are admin only if you're self-hosting, but there isn't any actual code to detect admin so make that yourself)

  -jace (designed to make fun of my friend who constantly plays tiktoks during match queues)

  -github (links to the github repos)