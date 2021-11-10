import re
from channels.db import database_sync_to_async
from django.db import close_old_connections

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
# from rest_framework_simplejwt.state import User
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from urllib.parse import parse_qs
from jwt import decode as jwt_decode
from django.conf import settings
from consultation.utils import get_consultation, verify_consultation_user, get_user


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner_app):
        self.inner_app = inner_app
        self.jwt_authenticator = JWTAuthentication()

    async def __call__(self, scope, receive, send):

        # close old database connections to prevent usage of timed out connections
        close_old_connections()
        # consultation_id
        consultation_id = parse_qs(
            scope['url_route']['kwargs']['consultation_id'])
        consultation = get_consultation(consultation_id)

        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as auth_error:
            return None
        else:
            # validate token
            decoded_data = self.jwt_authenticator.get_validated_token(token)
            # jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope["user"] = await get_user(decoded_token=decoded_data)

        return await super().__call__(scope, receive, send)