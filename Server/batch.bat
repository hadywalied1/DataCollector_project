ECHO ACTIVATING ENV 
..\env\Scripts\activate.bat
ECHO ACTIVATED 
set FLASK_ENV = development
set FLASK_APP = main
python -m flask run 
PAUSE