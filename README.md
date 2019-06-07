Yet Another Picture Presenter- YAPP
===================================

What is YAPP?
-------------
YAPP is a web based presentation software for party pictures. It is a new implementation of my first software version.

An unique feature of this software is the interaction and data exchange with the presentation software via common messenger application Telegram (https://telegram.org/). The implemented interface allows you following functions:

* Upload of pictures
* Download of pictures
* Voting
  * Add likes 
  * Add dislikes
* Renaming of pictures


Quick Start
-----------
Requirements:
* *docker* (https://docs.docker.com/install/)
* *docker-compose* (https://docs.docker.com/compose/install/)
* Telegram bot account (https://core.telegram.org/bots#3-how-do-i-create-a-bot) 


```
git clone https://github.com/h3nr1-g/Party-Picture-Presenter-2.git yapp

cd yapp/docker

# Replace in docker-compose.yml values of following environment variables: 
#   DJANGO_SECRET_KEY -> secret key for the different Django app instances
#   TELEGRAM_CONTACT -> Contact URL of the Telegram bot
#   TELEGRAM_TOKEN -> Auth token of the bot

docker-compose build 

docker-compose up

firefox http://127.0.0.1:8000
```

For the persistence of the received images and information the folder "~/yapp_data" will be created and stores all received pictures and the sqlite database.


Non Docker Usage, Dev and Testing
---------------------------------

Creation and usage of a virtual environment is advised: https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv
```
virtualenv venv -p $(which python3) && source venv/bin/activate

cd yapp

python manage.py runbroker --settings yapp.settings.testing
export TELEGRAM_CONTACT=http://t.me/MY-BOT-NAME && python manage.py runserver 0.0.0.0 --settings yapp.settings.testing
export TELEGRAM_TOKEN=MY-TELEGRAM-BOT-TOKEN && python manage.py runbot

```


