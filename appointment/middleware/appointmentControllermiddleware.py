from datetime import datetime
from django.utils import timezone
from channels.db import database_sync_to_async
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from django.conf import settings
import rest_framework.exceptions


class AppointmentChatMiddleware(BaseMiddleware):
    appointment_ws_path = r'api/v1/appointment/(?P<appointment_chat_id>\w+)/$'

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        # close old database connection to prevent usage of timed out connection
        close_old_connections()
        user = scope["user"]
        user_id = user.id
