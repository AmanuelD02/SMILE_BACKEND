from django.urls import re_path

from . import consumers

websocket_appointment_urlpatterns = [
    re_path(r'ws/appointment/?P<user_name>\w+)/$',
            consumers.ChatConsumer.as_asgi()),
]
