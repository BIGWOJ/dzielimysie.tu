from django.urls import re_path
from . import channels

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', channels.ChatConsumer.as_asgi()),
]