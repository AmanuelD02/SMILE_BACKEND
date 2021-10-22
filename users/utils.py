from rest_framework import serializers
from .models import User
import jwt
import datetime
import os

SECRET_KEY = os.getenv('JWT_SECRET')


class Utils:
    @staticmethod
    def encode_token(user: User):
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
        return token


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
