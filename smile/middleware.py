import re
from channels.db import database_sync_to_async
from django.db import close_old_connections
import rest_framework.exceptions
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
# from rest_framework_simplejwt.state import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from consultation.middleware.chatControllMiddleware import ChatControllMiddleware

from appointment.middleware.appointmentControllermiddleware import AppointmentChatMiddleware


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner
        self.jwt_authenticator = JWTAuthentication()

        # Appointment and Consultation Middlewares
        self.consultation_app = ChatControllMiddleware(inner)
        self.appointment_app = AppointmentChatMiddleware(inner)

    async def __call__(self, scope, receive, send):

        # close old database connections to prevent usage of timed out connections
        close_old_connections()

        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        AuthError = rest_framework.exceptions.AuthenticationFailed

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as auth_error:
            raise AuthError("Invalid Token")
        else:
            # validate token
            decoded_data = self.jwt_authenticator.get_validated_token(token)

            # jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope["user"] = await get_user(decoded_data)
            print(scope["user"])
            print(scope['path'])

        if bool(re.match(ChatControllMiddleware.consultation_ws_path, scope["path"])):
            print("Routing to the Consultation Middleware")
            return await self.consultation_app(scope, receive, send)
        elif bool(re.match(AppointmentChatMiddleware.appointment_ws_path, scope["path"])):
            print("Routing to the Appointment Middleware")
            return await self.appointment_app(scope, receive, send)
        else:
            print("Unrecognized Path")


@database_sync_to_async
def get_user(decoded_token):

    try:
        # User.objects.get(id=decoded_token['id'])
        return JWTAuthentication().get_user(decoded_token)
    except User.DoesNotExist:
        return None
