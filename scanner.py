import os, sys, time, signal, re, _thread
from datetime import datetime, timedelta
from contextlib import contextmanager
import vlc
import twint
import nest_asyncio
from io import StringIO

WELCOME_MSG = """\033[1m

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

def format_tweets(t):
    t = re.findall(r'<FredScanner>.*', t)
    t = '\n────────────────────────────────────\n'.join(t)
    t = re.sub(r'\s\s-\s.*', "", t)
    t = re.sub("<FredScanner>", "[Scanner]", t)
    return t

def merry_christmas(o):
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
    secret = input()
    if secret == "50":
        print("\n"*40)
        print(santa)
        print("\r    Merry Christmas Hambones...")
        print("           and Happy 50th      ")
        print(" I made this because you're always\n     wondering what's going on\n\toutside of the house")
        print("\n"*10)
        sys.stdout = None
        _thread.interrupt_main()
    else:
        _thread.interrupt_main()


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
    print("[Scanner] Loading feed...   ")
    loading_bar(3)
    t.Username = "FredScanner"
    now = datetime.today() - timedelta(hours=1, minutes=0)
    check_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print('[Scanner] Feed loaded...   \n', end='')
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
        new_tweets = format_tweets(result.getvalue())
        now = datetime.now()
        check_time = now.strftime("%Y-%m-%d %H:%M:%S")
        if new_tweets != '':
            print('\r', end='')
            print(new_tweets)
            print('─'*36)
            print(f"\r Last Checked: {check_time}", end='')
        else:
            print(f"\r Last Checked: {check_time}", end='')
        time.sleep(60)


def audio(source):
    vlc_instance = vlc.Instance("--quiet")
    scanner = vlc_instance.media_player_new()
    media = vlc_instance.media_new(source)
    scanner.set_media(media)

    print("[Scanner] Connecting to scanner...")
    loading_bar(5)

    try:
        scanner.play()
    except Exception as e:
        sys.exit(f"[Error] {e}")

    print("\r[Scanner] Connected to scanner...")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    if os.name == 'nt':
        os.system("mode con:cols=36 lines=40 & title Scanner & color 06 & cls")
    else:
        os.system("clear;printf '\\033[8;40;36t'")

    try:
        print(WELCOME_MSG)
        _thread.start_new_thread( tweets, (None, ) )
        _thread.start_new_thread( audio, ("https://broadcastify.cdnstream1.com/9809", ) )
        _thread.start_new_thread( merry_christmas, (None, ) )

    except:
        sys.exit("[Error] Threading Failure")

    while True:
        pass
