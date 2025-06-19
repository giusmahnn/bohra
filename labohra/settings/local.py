from .base import *
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True

ALLOWED_HOSTS = ['*']

# Base URL for the application
# This can be set in the .env file or defaults to localhost
# It is used for generating absolute URLs in the application.
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER")
HOST_USER_EMAIL = os.getenv('HOST_USER_EMAIL')



# Telegram token
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_URL = os.getenv("TELEGRAM_URL")