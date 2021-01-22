@echo off
python check-words.py strict
if %ERRORLEVEL%==1 goto end

python generate-tex-dictionary.py
python generate-tex-dictionary.py en

python generate-md.py
python generate-md.py en

python generate-wordlist.py

python generate-html-dictionary.py

cd small-andro-english-dictionary/
xelatex main.tex > NUL
cp -f main.pdf ../final/main-en.pdf
cd ..

cd small-andro-polish-dictionary/
xelatex main.tex > NUL
cp -f main.pdf ../final
cd ..

echo Done!

:end