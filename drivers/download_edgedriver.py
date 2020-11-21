#!/usr/local/bin/python3
import os
import sys
import struct
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://msedgedriver.azureedge.net"
this_os_architecture = struct.calcsize("P") * 8

if sys.platform.startswith('linux'):
    sys.exit("msedgedriver not available for Linux as of now.. please consider using Chrome or Firefox")

elif sys.platform.startswith('darwin'):
    this_os = 'darwin'
    zip_name = 'edgedriver_mac64.zip'

else:
    this_os = 'windows'
    zip_name = f'edgedriver_win{this_os_architecture}.zip'

edge_version = input(f"\nYour OS : {this_os}\nYour OS arch : {this_os_architecture}\n\nPlease go to 'edge://version' in your Edge browser and copy/paste the complete 'Microsoft Edge:' version number...\n> ")

try:
    f = requests.get(f"{BASE_URL}/{edge_version}/{zip_name}")
except:
    sys.exit("\nLook like you have entered the wrong Edge version number... Please try again!\n")
else:
    print(f.url)
    open(zip_name, 'wb+').write(f.content)
    if this_os == 'darwin':
        print("File downloaded succesfully in mac directory...")
        os.system(f"unzip {zip_name} -d temp_driver && rm edgedriver*.zip && chmod +x ./temp_driver/* && mv temp_driver/* mac/ && rm -rf temp_driver")
        print("\nAll done! Now you can run selenium scripts without a worry!")
    else:
        print("File downloaded successfully! Extract the binary (msedgedriver.exe) from the archive and move it to .\\drivers\\windows.")
