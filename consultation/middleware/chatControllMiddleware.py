from datetime import datetime
from django.utils import timezone
from channels.db import database_sync_to_async
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from django.conf import settings
from consultation.utils import get_user_wallet, check_user_balance
from rest_framework.exceptions import ValidationError

from consultation.tasks import terminate_consultation_chat


class ChatControllMiddleware(BaseMiddleware):
    consultation_ws_path = r"api/v1/consultation/consultation/(?P<consultation_chat_id>\w+)/$"

    def __init__(self, inner_app):
        self.inner_app = inner_app

    async def __call__(self, scope, receive, send):

        # close old database connection to prevent usage of timed out connection
        close_old_connections()
        user = scope["user"]
        user_id = user.id
        wallet = get_user_wallet(user_id)
        if wallet:
            consultation_id = scope["consultation_id"]
            time_capacity = check_user_balance(wallet, consultation_id)

            if time_capacity:
                stop_eta = datetime.now() + time_capacity
                terminate_consultation_chat.apply_async(
                    args=[consultation_id], eta=stop_eta)
                return await super.__call__(scope, receive, send)

            else:
                raise ValidationError(
                    "Balance is not enough to start Consultation.")
        else:
            raise ValidationError(
                "Invalid Wallet Information"
            )
