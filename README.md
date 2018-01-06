Party Picture Presenter 2 - PPP2
================================

What is PPP2?
-------------
PPP2 is a web based presentation software for party pictures. It is a new implementation of my first software version (https://github.com/h3nr1-g/PartyPicturePresenter).

An unique feature of this software is the interaction and data exchange with the presentation software via common messenger applications like Telegram (https://telegram.org/). The implemented interface allows you following functions:

* Upload of pictures
* Download of pictures
* Voting
* Renaming of pictures


How to install PPP2?
--------------------

```
git clone https://github.com/h3nr1-g/Party-Picture-Presenter-2.git

cd Party-Picture-Presenter-2

pip3 install -r requirements/base.txt

python3 manage.py makemigrations presenter && python manage.py migrate

python3 manage.py createsuper
```

How to configure PPP2?
----------------------
* Open with an editor the file *Party-Picture-Presenter-2/ppp2/ppp2/settings.py*

* Modify following entries:
    * SECRET_KEY (Modify for safty reasons)
    * ALLOWED_HOSTS (Add here the IP address of your machine)
    * MEDIA_ROOT (This will be the upload directory for new pictures)
    * BOT_CREDENTIALS (Enter here the authentication tokens for your bot accounts)
    * MAX_PICTURE_HEIGHT (Maximum height of a picture in the web browser)

Where can I get the tokens and bot accounts?
--------------------------------------------
* Telegram: https://core.telegram.org/bots

How to use PPP2?
----------------
* Start the presentation server:
```
bash Party-Picture-Presenter-2/ppp2/ppp2.sh
```

* Open a browser and open the overview page:
```
firefox http://127.0.0.1:8000
```

* Click on Live Mode and start the Live presentation in fullscreen or normal mode

* Open the Telegram messanger on your phone

* Start a conversation with the bot (you can find your bot via the search function)

* Send a photo to the bot

* The bot will confirm the reception and show it in the browser window


Further Documentation
---------------------
For further documentation take a look into HTML documentation (docs/build/html)
