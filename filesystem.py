                                #!/bin/env python3
from bs4 import BeautifulSoup
import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system('wget "https://www.mediafire.com/file/ow8hzyoevukxwkj/hardcodedAudio.zip/file"')

    soup = BeautifulSoup('file', 'html.parser')
    button = soup.find(id="downloadbutton", href=True)
    os.system(f"wget {button['href']}")
    

    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")