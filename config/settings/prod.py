
from .base import *
from decouple import config

# Debug settings
DEBUG = True

# Security settings
ALLOWED_HOSTS = ['*']  # Consider specifying your domain for production
APP_ENV = config('APP_ENV', default='prod')

DOMAIN_URL = "https://edlern.toolsfactory.tech/"
FRONTEND_DOMAIN_URL='edlern.vercel.app'
CORS_ALLOW_ALL_ORIGINS = True


#REDIS SETTING
REDIS_HOST ='localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# Celery settings for development
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = True  # Run tasks immediately (no worker needed)
CELERY_TASK_EAGER_PROPAGATES = True


# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

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
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'

# Django-storages settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'





CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": REDIS_PASSWORD,  # usually passed in URL, no need here
        }
    }
}
# Warning for in-memory channel layer
print("WARNING: Using InMemoryChannelLayer for prod testing. Not suitable for multi-user or production.")
