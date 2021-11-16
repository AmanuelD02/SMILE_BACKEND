"""
ASGI config for smile project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from smile.wsgi import *
from appointment.routing import websocket_appointment_urlpatterns
from consultation.routing import websocket_consultation_urlpatterns
from django.core.asgi import get_asgi_application
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path

from .middleware import TokenAuthMiddleware
from consultation.middleware.chatControllMiddleware import ChatControllMiddleware
from appointment.middleware.appointmentControllermiddleware import AppointmentChatMiddleware
from consultation.consumers import ChatConsumer as ConsultationChatConsumer
from appointment.consumers import ChatConsumer as AppointmentChatConsumer
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smile.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            #     [
            #     re_path(
            #         ChatControllMiddleware.consultation_ws_path,
            #         ConsultationChatConsumer.as_asgi(),
            #         name='ws-consultation'
            #     ),
            #     re_path(
            #         AppointmentChatMiddleware.appointment_ws_path,
            #         AppointmentChatConsumer.as_asgi(),
            #         name='ws-appointment'
            #     )
            # ]
            #
            # [url ]
            #websocket_consultation_urlpatterns + websocket_appointment_urlpatterns
            [
                re_path(r'api/v1/consultation/(?P<consultation_chat_id>\w+)/$',
                        ConsultationChatConsumer.as_asgi())
            ]
        )
    )
})
