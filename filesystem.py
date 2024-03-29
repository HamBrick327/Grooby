#!/bin/env python3
import requests
import shutil
from bs4 import BeautifulSoup
import os

url = "https://www.mediafire.com/file/tp6eult71hcsxwi/hardcodedAudio.zip/file"

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue") and not os.path.exists("./hardcoded"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    request = requests.get(url)
    content = request.content

    soup = BeautifulSoup(content, 'html.parser')
    button = soup.find('a', id="downloadButton")

    if button:
#         print("button is true")
        os.system(f"wget {button.get('href')}")
#    os.system(f"wget {button['href']}")
    else:
        print("button is flase")

    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")

## fixing windows zip files being werid because I'm lazy
if len(os.listdir()) == 1:
    shutil.move(os.path.join("./hardcodedAudio", "hardcodedAudio"), "./hardcodedAudio")
    os.rmdir(os.path.join("./hardcodedAudio", "hardcodedAudio"))