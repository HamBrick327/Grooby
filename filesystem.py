#!/bin/env python3

import os

## check if ./queue directory exists, if not, create it
if not os.path.exists("./queue"):
    os.mkdir("./queue")
    os.mkdir("./hardcodedAudio")
    os.system("wget https://download1076.mediafire.com/zjpcdkwdm5dgLP_O-y6GT6Ajl2Tdm-HVkf_EuKBCbqA59O5qsz0AF_rpBXaetaQN4XemNyAA_RKnvJF8rObQ9zTIp11_eJNQsZRSNXVpWOwhxSlN4umce1SW_LdBBcn5pKy8SwfOebuw9ESYuhmpZHxn4Wn9H9rj5k-XQdA/i7gwkmyqsaw8b20/hardcodedAudio.zip")
    os.system("unzip hardcodedAudio.zip -d ./hardcodedAudio")
    os.remove("./hardcodedAudio.zip")