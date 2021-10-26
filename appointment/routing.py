from django.urls import re_path, path

from . import consumers

websocket_appointment_urlpatterns = [
    path('ws/appointment/<int:appointment_id>/',
            consumers.ChatConsumer.as_asgi()),
]
