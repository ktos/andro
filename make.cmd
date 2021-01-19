@echo off
python check-words.py strict
if %ERRORLEVEL%==1 goto end

python generate-tex-dictionary.py
python generate-tex-dictionary.py en

python generate-md.py
python generate-md.py en

python generate-wordlist.py

python generate-html-dictionary.py

:end