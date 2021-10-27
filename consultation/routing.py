from django.urls import re_path

from . import consumers

websocket_consultation_urlpatterns = [
    re_path(r'ws/consultation/?P<consultation_chat_id>\w+)/$',
            consumers.ChatConsumer.as_asgi()),
]
