#!/bin/env python3

import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system("wget https://download1076.mediafire.com/loc5k90txm5gcDtOyfOYzbTR7wIUEGmEgyuI7DWmNEmxjfMi_Ldr07ONmxrmRFglV34v0pnz3EFnatyfp6SeMJmo3-ID_GU4z1V9dnTxROTJL0JyMixk9ndbU0noHGb07FbTR4zP9rOvgqw_V_V8_7v8m8HGpKsdzhKxRvs/i7gwkmyqsaw8b20/hardcodedAudio.zip")
    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.system("rm hardcodedAudio.zip")
