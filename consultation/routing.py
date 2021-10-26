from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/consultation/?P<user_name>\w+)/$',
            consumers.ChatConsumer.as_asgi()),
]
