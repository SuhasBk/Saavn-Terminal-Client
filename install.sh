chmod 777 -R .;

echo '*This installation script is for Linux users only.* Use this script to automatically set-up all dependencies required to run saavn.py';

sleep 5;
wget "https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz";
tar -xvf gecko*;
rm gecko*.tar.gz

echo 'The file has been successfully downloaded. Please enter the password to put it in the path...';
sleep 2;

sudo mv gecko* /usr/local/bin/;

echo 'You are all set! Enjoy Saavn...'
