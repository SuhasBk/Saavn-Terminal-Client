#!/usr/bin/python3
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChrOptions
from selenium.webdriver.firefox.options import Options as FireOptions
import selenium,time,string,sys,os,re,random,requests,qrcode
from bs4 import BeautifulSoup
from subprocess import run,PIPE

# global variables
browser = None
pause = 0
rep = 0

#  Start working in background while waiting for user input
def initialize():
    try:
        print('Welcome To Saavn Terminal Client!')
        global browser
        if len(sys.argv)>1:
            #browser = webdriver.Chrome()
            browser = webdriver.Firefox()
        else:
            opt = FireOptions()
            #opt = ChrOptions()
            opt.headless=True
            #browser = webdriver.Chrome(options=opt)
            browser = webdriver.Firefox(options=opt)
    except:
        exit("\nSomething's fishy...")

# backdoor entry for debugging purposes
def debug():
    while(True):
        try:
            cmd=input("Enter the debugging commands...\n")
            if cmd=='exit' or cmd=='':
                return
            exec(cmd)
        except:
            print('NOT WORKING!')
            pass

# browser control
def handler():
    try:
        browser.execute_script("Player.setBitrate({});".format(128))
        def lang():
            browser.execute_script("Header.changeLanguage('{}');".format(input("Enter language preference..\n").lower()))
            return

        def new():
            song_name = '+'.join(input("Enter the song name you want to listen to.... Type 'q' to go back\n> ").split())
            if song_name == 'q':
                pass
            else:
                navigate(song_name)

        def next():
            fwd = browser.find_element_by_id('fwd')
            browser.execute_script("arguments[0].click();",fwd)
            print("\nPlaying next song...\n")
            return

        def play_pause():
            global pause
            if pause==0:
                pause = 1
                p = browser.find_element_by_id('pause')
            elif pause==1:
                pause = 0
                p = browser.find_element_by_id('play')
            browser.execute_script("arguments[0].click();",p)
            return

        def prev():
            rew = browser.find_element_by_id('rew')
            browser.execute_script("arguments[0].click();",rew)
            print("\nPlaying the last song....\n")
            return

        def info():
            print("\nTrack name : "+browser.find_element_by_id('player-track-name').text+' from the album -  '+browser.find_element_by_id('player-album-name').text)
            print("\nTrack duration : "+browser.find_element_by_id('track-time').text)
            print("\nElapsed time : "+browser.find_element_by_id('track-elapsed').text)
            return

        def top():
            print('\nStopping current playback...\n')
            browser.get('https://jiosaavn.com')
            a = browser.find_elements_by_class_name('x-small')[1]
            browser.execute_script("arguments[0].click()",a)
            time.sleep(5)
            browser.find_element_by_class_name('play').click()

        def repeat():
            global rep
            button = browser.find_element_by_id('repeat')
            if rep==0:
                rep=1
                browser.execute_script('arguments[0].click();',button)
                print('\nRepeat mode ON\n')
            elif rep==1:
                rep=0
                for i in range(0,2):
                    browser.execute_script('arguments[0].click();',button)
                print('\nRepeat mode OFF\n')
            return

        def lyrics(name):
            r=requests.get("https://search.azlyrics.com/search.php?q="+'+'.join(name.split()),headers={'User-Agent':'MyApp'})
            s=BeautifulSoup(r.text,'html.parser')
            td=s.findAll('td',attrs={'class':'text-left visitedlyr'})
            res=[]

            if len(td) == 0:
                custom = input("No results found for this...Want to try again with user-defined search? (y)\n")
                if custom =='y':
                    lyrics(input("\nOkay... Enter the user-defined song name...\n"))
                    return
                else:
                    print('\nOkay... returning to main menu...\n')
                    return

            for i,j in enumerate(td):
                s=re.findall(r'<b>.*</b>',str(j))[0]
                for r in (('<b>',''),('</b>',''),('</a>','')):
                    s=s.replace(*r)
                print(i,s)
                res.append(j.find('a').get('href'))

            choice = input("\nChoose one from above : (type 'exit' to go back to previous menu)\n")

            for i,j in enumerate(res):
                if choice==str(i):
                    q=requests.get(j,headers={'user-agent':'MyApp'})
                    s=BeautifulSoup(q.text,'html.parser')
                    l=s.find('div',attrs={'class':'col-xs-12 col-lg-8 text-center'})
                    try:
                        print(l.find('div',attrs={'class':''}).text)
                    except AttributeError:
                        print('\nOops! Requested lyrics not available...\n')
                elif choice == 'exit':
                    return
            return

        def share():
            share = browser.find_elements_by_class_name('outline')[3]
            browser.execute_script("arguments[0].click();",share)
            inp = browser.find_elements_by_tag_name('input')
            link = inp[len(inp)-1].get_attribute("value")
            print("Share this link or scan the QR code :- {}".format(link))
            img = qrcode.make(link)
            img.show()

        def download():
            search_term = browser.find_element_by_id('player-track-name').text
            print("Fetching results for "+search_term)
            r = requests.get("http://youtube.com/results?search_query=" + '+'.join(search_term),headers={'User-Agent':'random_stuff'})

            print("Searching....")
            s = BeautifulSoup(r.text, 'html.parser')
            l = s.select('div .yt-lockup-content')

            urls = []
            titles = []

            try:
                for i in l:
                    urls.append('http://youtube.com'+i.find('a').get('href'))
                    titles.append(i.find('a').get('title'))
            except:
                pass

            length = len(l)
            if len(l) > 5:
                length = int(len(l)*0.50)   #  show only 50% of results

            for i,t,u in zip(range(length),titles,urls):
                print('\n',i,t.upper(),'\nYouTube URL : ',u)

            ch = input("Choose from the above : ('exit' to go back)\n> ")

            for i,j in enumerate(urls):
                if ch==str(i):
                    op = run("youtube-dl --extract-audio --audio-format mp3 "+j,shell=True,stderr=PIPE)
                    error = op.stderr.decode('utf-8')
                    if error != '':
                        if 'ffprobe/avprobe' in error:
                            pass
                    else:
                        print(error)
                elif ch == 'exit':
                    print("\nDownload aborted!")
                    return

            print("Successfully Downloaded {}".format(search_term))
            return

        def cya():
            exit('Stopping playback...Closing Saavn...')

        def default():
            print('Wrong Choice!\n')
            return

        routes = {'1':new,'2':next,'3':play_pause,'4':prev,'5':info,'6':top,'7':repeat,'8':lyrics,'9':lang,'10':share,'11':download,'13':debug,'12':cya,'default':default}

        while True:
            time.sleep(0.5)
            print("\nTrack name : "+browser.find_element_by_id('player-track-name').text+' from the album - '+browser.find_element_by_id('player-album-name').text+'\n')

            ch = input("\n'1' : New Song\n'2' : Next Song\n'3' : Play/Pause\n'4' : Previous Song\n'5' : Song Info\n'6' : Top Songs This Week (based on language preference)\n'7' : Repeat Current Song\n'8' : Lyrics for Current Song\n'9' : Change Language (current language : {0})\n'10' : Share this song...\n'11' : Download current song... (requires 'youtube-dl')\n'12' : Close Saavn...\n\nEnter your choice...\n> ".format(browser.find_element_by_id('language').text))

            if ch in routes:
                if ch == '8':
                    name = browser.find_element_by_id('player-track-name').text

                    if input("The current search paramter is '{}'. Do you want to continue ('n') or refine it? ('y')\n> ".format(name)) == 'y':
                        name = input("Enter the search term...\n> ")
                        print("Okay... Searching for {}...".format(name))
                    else:
                        print("Searching for {}...".format(name))

                    routes[ch](name)
                else:
                    routes[ch]()
            else:
                routes['default']()

    except selenium.common.exceptions.ElementClickInterceptedException:
        browser.find_element_by_tag_name('html').send_keys(Keys.ESCAPE)
        print('\nPlease select again... Sorry for minor inconvenience\n')
        handler()

# navigating around saavn
def navigate(song_name):
    #  if Python's too slow ;)
    if init.is_alive():
        init.join()

    #  if user is feeling bored to type
    if song_name == '':
        print("\nPlaying this week's top songs...\n")
        browser.get('http://jiosaavn.com/')
        a = browser.find_elements_by_class_name('x-small')[1]
        browser.execute_script("arguments[0].click()",a)
        time.sleep(5)
        browser.find_element_by_class_name('play').click()
    else:
        try:
            print("\nSearching for "+' '.join(song_name.split('+'))+'...')
            browser.get('http://jiosaavn.com/search/{}'.format(song_name))
        except:
            browser.quit()
            sys.exit('\nCheck your internet connection and try again...\n')

        # logic to start playback:
        titles = browser.find_elements_by_class_name('title')
        meta = browser.find_elements_by_class_name('meta-album')

        #  selects random track:
        # browser.execute_script("arguments[0].click()",random.choice(titles).find_element_by_tag_name('a'))

        if len(titles) < 1:
            browser.quit()
            exit('Oops! No results found!')

        # remove ad in between songs:
        #ad = browser.find_element_by_id('ad-drawer')
        #browser.execute_script("arguments[0].remove();",ad)

        for i,j,k in zip(list(range(len(titles))),titles,meta):
                print(i,j.text,' : ',k.text)

        ch = input("\nEnter your choice ('exit' to quit and 'q' to return):\n> ")
        for i,j in enumerate(titles):
            if ch==str(i):
                browser.execute_script("arguments[0].click();",j.find_element_by_tag_name('a'))
            elif ch=='':
                browser.execute_script("arguments[0].click();",titles[0].find_element_by_tag_name('a'))
            elif ch=='exit':
                return
            elif ch=='q':
                return

        time.sleep(3)
        song = browser.find_element_by_class_name('play')
        try:
            song.click()
        except:
            browser.execute_script('arguments[0].click();',song)
    handler()

if __name__ == '__main__':
    try:
        init = Thread(target=initialize)
        init.start()
        #  entry message and user input
        try:
            song_name = '+'.join(input("Enter the song name you want to listen to....\n> ").split())
            print("Connecting to Saavn...\n")
        except:
            try:
                browser.quit()
                os.remove('geckodriver.log')
            except:
                pass
            exit('\nConnection aborted\n')
        navigate(song_name)
    finally:
        try:
            browser.quit()
            os.remove('geckodriver.log')
            exit("Thank you for using this software")
        except:
            pass
