from yapp.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'NOT_SO_SECRET'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}