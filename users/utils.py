from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
import os

SECRET_KEY = os.getenv('JWT_SECRET')


class Utils:
    @staticmethod
    def encode_token(user: User):
        payload = {
            'id': user.id,
            'role': user.role,
        }
        token = RefreshToken.for_user(user)
        token.payload['TOKEN_TYPE_CLAIM'] = 'access'
        #token = jwt.encode(payload, "SNAKE_POO", algorithm='HS256')
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

    @staticmethod
    def decode_token(encoded_jwt, secret):

        response = JWT_authenticator.authenticate(request)
        decoded_value = jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
        return decoded_value


def update_user_account(full_name, phone_num, role, date_of_birth, bio, profile_pic_path, slug, username=None):
    user = User.objects.filter(phone_num=phone_num).update(
        full_name=full_name,
        role=role,
        date_of_birth=date_of_birth,
        bio=bio,
        profile_pic_path=profile_pic_path,
        slug=slug
    )

    return user
