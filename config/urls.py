
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_VERSION='v1'

urlpatterns = [
    path('platform-admin/', admin.site.urls),
    path(f'api/{API_VERSION}/accounts/', include('apps.accounts.urls')),
    path(f'api/{API_VERSION}/auth/', include('apps.authentication.urls')),
    path(f'api/{API_VERSION}/community/', include('apps.community.urls')),
    path(f'api/{API_VERSION}/classroom/', include('apps.classroom.urls')),
    path(f'api/{API_VERSION}/calendar/', include('apps.calendar.urls')),
    path(f'api/{API_VERSION}/common/', include('apps.core.urls')),
    path(f'api/{API_VERSION}/market_place/', include('apps.market_place.urls')),
    path(f'api/{API_VERSION}/chats/', include('apps.chats.urls')),
    path(f'api/{API_VERSION}/gamification/', include('apps.gamification.urls')),
    path(f'api/{API_VERSION}/notifications/', include('apps.notifications.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    