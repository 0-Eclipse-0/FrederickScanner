import os
import time
from datetime import datetime
import vlc

welcome_msg = """
  ___           _         _    _
 | __| _ ___ __| |___ _ _(_)__| |__
 | _| '_/ -_) _` / -_) '_| / _| / /
 |_||_| \___\__,_\___|_| |_\__|_\_\\
 / __| __ __ _ _ _  _ _  ___ _ _
 \__ \/ _/ _` | ' \| ' \/ -_) '_|
 |___/\__\__,_|_||_|_||_\___|_|
             By: Matt
"""

#try:
#    import vlc
#except ModuleNotFoundError:
#    os.system("pip install python-vlc")
#    import vlc

if os.name == 'nt':
    os.system("mode con:cols=36 lines=40 & title Scanner & color 06 & cls")
else:
    os.system("clear; printf '\\033[8;40;36t'")

print(welcome_msg)

scanner = vlc.MediaPlayer("https://broadcastify.cdnstream1.com/9809")
scanner.play()

while True:
    pass
