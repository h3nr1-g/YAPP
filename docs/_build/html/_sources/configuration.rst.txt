Set Up & Configuration
~~~~~~~~~~~~~~~~~~~~~~

In order to get PPP2 up and running please execute the following commands:

1. Create the Bot account(s):
   
   * Telegram: Link_  

2. Prepare the Django Web Application Framework 

.. code-block:: bash

   cd Party-Picture-Presenter-2/ppp
   python3 manage.py makemigrations presenter
   python3 manage.py migrate 
   python3 manage.py createsuperuser

3. Edit the configuration file settings.py

.. code-block:: python

   # Choose a new secret key
   SECRET_KEY = 'SECRET_KEY' 
   ...

   # Add here the IP address(es) of the system
   ALLOWED_HOSTS = []
   ...
   
   # Change the upload directory for incoming pictures
   MEDIA_ROOT = os.path.realpath(os.path.join(BASE_DIR, '..', '..', 'uploads'))
   ...
   
   # Adapt the presentation settings
   SECONDS_PER_PICTURE = 10
   BACKGROUND_COLOR = 'black'
   TITLE_FONT_COLOR = 'white'
   MAX_PICTURE_HEIGHT = 800
   ...

   # Enter your bot credentials and tokens
   BOT_CREDENTIALS = {
      'Telegram': 'MY_SECRET_TELEGRAM_TOKEN'
   }

4. Start the HTTP server and all subcomponts 

.. code-block:: bash

   bash ppp2.sh

.. _Link: https://core.telegram.org/bots
