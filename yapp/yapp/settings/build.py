from yapp.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DOES_NOT_MATTER'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}