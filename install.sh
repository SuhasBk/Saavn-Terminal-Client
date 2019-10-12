chmod 777 -R .;

echo -e '*This installation script is for Linux users only.*\nUse this script to automatically set-up all dependencies required to run saavn.py';

sleep 5;
wget "https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz";
tar -xvf gecko*;
rm gecko*.tar.gz

echo -e '\nThe file has been successfully downloaded. Please enter the password to put it in the path...';
sleep 2;

sudo mv gecko* /usr/local/bin/;

echo -e '\nCool! Everything is ready now... Do you want to automatically install requirements using *pip* as well?\n'

read ans
if [ $ans == "y" ]||[ $ans == 'Y' ]
then
    python3 -m pip install --user -r requirements.txt;
else
    echo -e '\nYou are all set! Enjoy Saavn...';
fi;
