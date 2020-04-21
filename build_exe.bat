@ECHO OFF
del saavn.exe
pyinstaller saavn.py --onefile --add-binary ".\drivers\windows\geckodriver.exe;.\drivers\windows" --add-binary ".\drivers\windows\chromedriver.exe;.\drivers\windows"
copy dist\saavn.exe .
del saavn.spec
rmdir /S /Q build dist