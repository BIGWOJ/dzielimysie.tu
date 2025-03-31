"""
ASGI config for dzielimysie_tu project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
import django

# Ustawienie zmiennej środowiskowej dla Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dzielimysie_tu.settings')

# Inicjalizacja Django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

# Konfiguracja aplikacji ASGI
application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})