from django.core.wsgi import get_wsgi_application
from decouple import config
import os

# Load the correct .env file
APP_ENV = config('APP_ENV', default='local')
print("my app env is", APP_ENV)

if APP_ENV == "local":
    print("loading local settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
elif APP_ENV == "prod":
    print("loading prod settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
else:
    print("loading dev settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# Load the application
application = get_wsgi_application()