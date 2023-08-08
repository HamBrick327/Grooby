#!/bin/env python3

import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system('python3 mfdl.py ./ "https://www.mediafire.com/file/ow8hzyoevukxwkj/hardcodedAudio.zip/file"')
    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")