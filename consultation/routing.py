from django.urls import re_path, path

from . import consumers

websocket_consultation_urlpatterns = [
    path(r'api/v1/consultation/(?P<consultation_chat_id>\w+)/$',
         consumers.ChatConsumer.as_asgi()),
]
