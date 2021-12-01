import os, sys, time, signal, re, _thread
from datetime import datetime, timedelta
from contextlib import contextmanager
import vlc
import twint
import nest_asyncio
from io import StringIO

welcome_msg = """\033[1m

           ,▄███▀▀▀▀███▄,
        ▄█▀▀¬          '╙▀█▄
      ▄█▀                  ╙█▄
     █▀                      ╙█µ
    █▌                        ╙█
   ║█                          ║█
   █▌                          ▐█
   ██L ▄      Frederick     ▄ ]██
 ┌███▌ █⌐      Scanner      █ ▐███▄
▐████▌ █⌐                   █ ▐████▌
▐████▌ █⌐ [Matt Hambrecht]  █ ▐████▌
 ████▌ █⌐                   █ ▐███▌
 █▌╙▀▌ █                    ▀ ▐▀▀¬
 ╙█▄
   ╙█▄
     ╙█▄     ,,,
       ╙▀██φ█████▌
            ╙▀▀▀▀
"""

nest_asyncio.apply()
t = twint.Config()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

def signal_handler(sig, frame):
    print("\r[Scanner] Exitting...", ' '*14)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if os.name == 'nt':
    os.system("mode con:cols=36 lines=40 & title Scanner & color 06 & cls")
else:
    os.system("clear;printf '\\033[8;40;36t'")

print(welcome_msg)

def merry_christmas():
    santa = """
              ____
           {} _  \\
              |__ \\
             /_____\\
             \o o)\)_______
             (<  ) /#######\\
           __{'~` }#########|
          /  {   _}_/########|
         /   {  / _|#/ )#####|
        /   \_~/ /_ \  |#####|
        \______\/  \ | |####|
         \__________\|/#####|
          |__[X]_____/ \###/
          /___________\\
           |    |/    |
           |___/ |___/
          _|   /_|   /
         (___,_(___,_)
          """
    print(santa)
    print("\rMerry Christmas Hambones...")
    sys.exit(0)

def loading_bar(stime):
    i=1
    j=1
    bp = '■'
    while i < 11:
        while j < 11:
            percent = (i-1)*10 + j
            print("\r\t["+bp*i+(" "*(10-i))+"] "+f"({percent}%)", end='')
            time.sleep(stime/100)
            j += 1
        i += 1
        j = 1
    print('\r', end='')

def tweets(o):
    time.sleep(9)
    print("[Scanner] Loading feed...")
    loading_bar(3)
    t.Username = "FredScanner"
    now = datetime.today() - timedelta(hours=0, minutes=30)
    check_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print('[Scanner] Feed loaded...   \n', end='')
    running = False
    while True:
        t.Since = check_time
        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result
        twint.run.Search(t)
        sys.stdout = old_stdout
        if running == False:
            print('─'*36)
            running = True
        new_tweets = result.getvalue()
        new_tweets = re.findall(r'<FredScanner>.*', new_tweets)
        new_tweets = '\n────────────────────────────────────\n'.join(new_tweets)
        new_tweets = re.sub(r'\s\s-\s.*', "", new_tweets)
        new_tweets = re.sub("<FredScanner>", "[Scanner]", new_tweets)
        now = datetime.now()
        check_time = now.strftime("%Y-%m-%d %H:%M:%S")
        if new_tweets != '':
            print('\r', end='')
            print(new_tweets)
            print('─'*36)
            print(f"\r Last Checked: {check_time}", end='')
        else:
            print(f"\r Last Checked: {check_time}", end='')
        time.sleep(10)


def audio(source):
    vlc_instance = vlc.Instance("--quiet")
    scanner = vlc_instance.media_player_new()
    media = vlc_instance.media_new(source)
    scanner.set_media(media)

    print("[Scanner] Connecting to scanner...")
    loading_bar(5)

    try:
        with suppress_stdout():
            scanner.play()
    except Exception as e:
        sys.exit(f"[Error] {e}")

    print("\r[Scanner] Connected to scanner...")

try:
    _thread.start_new_thread( tweets, (None, ) )
    _thread.start_new_thread( audio, ("https://broadcastify.cdnstream1.com/9809", ) )
except:
    sys.exit("[Error] Threading Failure")

while True:
    pass
