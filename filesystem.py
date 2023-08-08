#!/bin/env python3

import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system("wget https://download1076.mediafire.com/71czlj4ptqqg24i4Sh85UB4jUaVYSEHykUTVGTY1dE7bhel2wI1vAhN-BSWivLRmgdg5f5jygahToMvDOCF7lE1vIxcPSIrIUAAdCnbE7cLqqJPSy25DY9LKOUGiS7jaBabsY6MH8nSDrluByhhIpC8CJz_xPMdVzYmWY-o/ow8hzyoevukxwkj/hardcodedAudio.zip")
    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")