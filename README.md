How to build and run:

 - Install python3
 
 https://www.python.org/downloads/
 - Install virtualenv
```
 pip install virtualenv
```

 - Clone the repo
```
git clone https://github.com/UniBanker/byzantine.git
cd byzantine
```
 - Create a virtualenv
```
virtualenv venv
```
 - Activate the virtualenv
```
source venv/Scripts/activate
```
 - Install dependencies
```
pip install -r requirements.txt
```
 - Run the updater
```
python updater.py
```
 - Run the webapp (DEBUG)
```
cd app
env FLASK_APP=main.py flask run
```

 - Run the webapp (PROD)
 ```
 gunicorn app:app -b 0.0.0.0:8020 --chdir ..
 ```