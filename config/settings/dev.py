from .base import *
from decouple import config

# Debug settings
DEBUG = True
ALLOWED_HOSTS = ['*']

# Environment
APP_ENV = config('APP_ENV', default='dev')
FRONTEND_DOMAIN='smartcandid.toolsfactory.tech'
# Additional apps for development
INSTALLED_APPS += [
    'django_celery_results',
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Database (PostgreSQL with Supabase)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.fycbudvzuqdcfdmynala',
        'PASSWORD': 'kYkRbIcU3da8YM90',
        'HOST': 'aws-0-ap-south-1.pooler.supabase.com',
        'PORT': '5432',
    }
}

# URLs
DOMAIN_URL = "https://edlern.weepul.in.net"

# Celery settings for development
CELERY_BROKER_URL = 'memory://'  # In-memory broker
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks immediately (no worker needed)
CELERY_TASK_EAGER_PROPAGATES = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='thequickaiii@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='gxvvjlsyfzngrzsx')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='no-reply@thequickai.com')

# AWS S3 Storage
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None  # Use bucket policy for access control
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'

# Django-storages settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'



CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Cache (in-memory)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
}
# Warning for in-memory channel layer
print("WARNING: Using InMemoryChannelLayer for dev testing. Not suitable for multi-user or production.")