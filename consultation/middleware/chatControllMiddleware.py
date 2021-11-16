from datetime import datetime
from django.utils import timezone
from channels.db import database_sync_to_async
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from django.conf import settings
from consultation.utils import get_user_wallet, check_user_balance
import rest_framework.exceptions

from consultation.tasks import terminate_consultation_chat
from consultation.utils import get_consultation, verify_consultation_user


class ChatControllMiddleware(BaseMiddleware):
    consultation_ws_path = r"/api/v1/consultation/(?P<consultation_chat_id>\w+)/$"

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        # close old database connection to prevent usage of timed out connection
        close_old_connections()
        user = scope["user"]
        print(scope)
        # scope['url_route']['kwargs']['consultation_chat_id']
        chat_id = "43184bc9891e48e7b0ee7f992ddebd83"
        user_id = user.id
        consultation = get_consultation(chat_id)

        AuthError = rest_framework.exceptions.AuthenticationFailed
        if user:
            if consultation:
                if verify_consultation_user(consultation, user):
                    wallet = get_user_wallet(user_id)
                    if wallet:
                        consultation_id = chat_id  # scope["consultation_id"]
                        time_capacity = await check_user_balance(
                            wallet, consultation_id)

                        if time_capacity:

                            stop_eta = datetime.now() + time_capacity  # datetime(2021, 11, 15)
                            terminate_consultation_chat.apply_async(
                                args=[consultation_id], eta=stop_eta)
                            return await self.inner(scope, receive, send)

                        else:
                            raise ValidationError(
                                "Balance is not enough to start Consultation."
                            )

                    else:
                        raise ValidationError(
                            "Invalid Wallet Information"
                        )
                else:
                    raise AuthError("Unauthorized Access")
            else:
                raise rest_framework.exceptions.ValidationError(
                    "Invalid Consultation Information")
        raise AuthError("Invalid User Information")
