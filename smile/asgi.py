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
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smile.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            #
            websocket_consultation_urlpatterns + websocket_appointment_urlpatterns
        )
    )
})
