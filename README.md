# Saavn_Terminal_Client

A Python browser-automation CLI to search for, listen to, download and share songs from [Saavn](http://jiosaavn.com).

Usage : saavn.py -b/--browser \[chrome | firefox | edge]  -d/--debug \[on | off]*

\*debug_mode : If set to 'off', the browser will run in background. If set to 'on', the user can interact with the browser.

To satisfy dependencies, run :
pip install -r requirements.txt

Additional dependencies:
1) Chrome browser (version >= 78) OR Firefox (version >= 70) OR Microsoft Edge (version >= 85)
2) chromedriver for Chrome / geckodriver for Firefox -> download using the Python scripts provided in ./drivers/

Note : If you encounter errors, update your browser and/or try using the latest [geckodriver](https://github.com/mozilla/geckodriver/releases) or [chromedriver](https://chromedriver.chromium.org/downloads) or [msedgedriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).
This is not an official Saavn product nor endorsed by Saavn.
