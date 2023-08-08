#!/bin/env python3
import requests
from bs4 import BeautifulSoup
import os

url = "https://www.mediafire.com/file/ow8hzyoevukxwkj/hardcodedAudio.zip/file"

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
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
