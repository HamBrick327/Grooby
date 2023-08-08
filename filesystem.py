#!/bin/env python3

import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system("wget https://download1076.mediafire.com/58g5msotwoygKzJQA2qaDLiw_8EsPaAlihGFyYKw3yA5sYOnIBMptMygDtGJRGpfnd01ee6HDi4_Q9WLEGbws1LNyemUA64-8vvLPwrcWhmlz7Eeg9FPX4_BWUSTBDUMnQWDVwJVk8sImSPexc1YdRBwNj7qeTs98vLNf-Q/i7gwkmyqsaw8b20/hardcodedAudio.zip")
    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")