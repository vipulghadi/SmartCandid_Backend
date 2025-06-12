import os
from celery import Celery
from decouple import config


# Set default settings module for 'celery'
APP_ENV = config('APP_ENV', default='dev')

if APP_ENV == "local":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
elif APP_ENV == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()