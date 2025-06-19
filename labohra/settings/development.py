from .base import *
import os
from dotenv import load_dotenv

load_dotenv()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT', 5432),
         'OPTIONS': {
             'sslmode': 'require',
        }
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