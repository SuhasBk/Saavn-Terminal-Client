#!/usr/bin/python3

import requests
import os
import sys
from bs4 import BeautifulSoup

if sys.platform.startswith('linux'):
    this_os = 'linux'
    zip_name = 'chromedriver_linux64.zip'
elif sys.platform.startswith('darwin'):
    this_os = 'darwin'
    zip_name = 'chromedriver_mac64.zip'
else:
    this_os = 'windows'
    zip_name = 'chromedriver_win32.zip'

session = requests.Session()
r = session.get("https://chromedriver.chromium.org/downloads")
s = BeautifulSoup(r.text,'html.parser')
 
versions = s.findAll('a',{'style':'background-color:transparent','target':'_blank'})
version_links = list(map(lambda x: x.get('href').replace('index.html?path=','')+zip_name,versions))
version_numbers = list(map(lambda x:x.text[:x.text.find('.')].replace('ChromeDriver ',''),versions))

downloads = dict(zip(version_numbers,version_links))

for k,v in downloads.items():
    print(k," : ",v)

ch = input("Enter the your Chrome browser version:\n> ")

try:
    download_url = downloads[ch]

    f = session.get(download_url)
    open(zip_name,'wb+').write(f.content)
    
    if this_os == 'linux':
        print("File downloaded succesfully in linux directory...")
        os.system(f"unzip {zip_name} && rm chromedriver*.zip && chmod +x chromedriver && mv chromedriver linux/")
        print("\nAll done! Now you can run selenium scripts without a worry!")
    elif this_os == 'darwin':
        print("File downloaded succesfully in mac directory...")
        os.system(f"unzip {zip_name} && rm chromedriver*.zip && chmod +x chromedriver && mv chromedriver mac/")
        print("\nAll done! Now you can run selenium scripts without a worry!")
    else:
        print("File downloaded successfully! Extract the binary from the archive and add its location to the PATH variable.")
except KeyError:
    sys.exit("Please choose from the list!")
finally:
    session.close()
