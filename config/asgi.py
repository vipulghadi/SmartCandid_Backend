
import os
from decouple import config


APP_ENV = config('APP_ENV', default='local')
print("my app env in asgi is", APP_ENV)

if APP_ENV == "local":
    print("loading local settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
elif APP_ENV == "prod":
    print("loading prod settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
else:
    print("loading dev settings")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# MUST call this before using models or anything Django-related
import django
django.setup()

# Now safe to import Django-dependent components
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chats.routing import websocket_urlpatterns
from apps.core.middlewares.community_chat_middleware import JWTAuthMiddlewareCommunityChat

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  
    "websocket":  JWTAuthMiddlewareCommunityChat(URLRouter(websocket_urlpatterns))
})
