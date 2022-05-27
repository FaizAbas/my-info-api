# my-info-api
Personal Project

## MyInfo Python API Integration Usage

Set up virtualenv

```shell script
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Run the Django Server

```shell script
./manage.py makemigrations
./manage.py migrate
./manage.py runserver 3001
```

Open up a browser and navigate to http://localhost:3001/callback/start

After clicking on the green "I Agree" button, you'll be redirected back to a url like blow
http://localhost:3001/callback?code=25e3a9679bfc9baca7ef47bceadea43fcd6eb199&state=blahblah
You will then see the response from My Info API rendered onto html using Django Template
