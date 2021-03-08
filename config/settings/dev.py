from config.settings.base import INSTALLED_APPS
from config.settings.base import *
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

if os.environ.get("ENV_PATH"):
    env_path = os.environ.get("ENV_PATH")
    load_dotenv(dotenv_path=env_path)

DEBUG = True
DOMAIN = 'http://localhost:8005'
# SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PWD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware',)

ALLOWED_HOSTS = ['*']
