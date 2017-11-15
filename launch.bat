REM run the node and bower updates
REM CMD /c npm install
REM CMD /c bower install
CMD /c npm update
CMD /c bower update

CMD /c pip install -r requirements.txt
REM run the migration updates
CMD /c python db.py db upgrade

REM start the applications
START "" npm start
START "" python run.py

REM give the applications a few seconds to start before opening a browser
TIMEOUT 5
START "" "chrome.exe" "http://localhost:4000"