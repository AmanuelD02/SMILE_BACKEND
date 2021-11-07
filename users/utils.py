from rest_framework import serializers
from .models import User
from payment.models import Contact
from payment.serializers import ContactSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET')
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_CONTACT_ENDPOINT = os.getenv('RAZORPAY_CONTACT_ENDPOINT')
RAZORPAY_FUND_ACCOUNT_ENDPOINT = os.getenv('RAZORPAY_FUND_ACCOUNT_ENDPOINT')


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

    @staticmethod
    def generateOTP():
        return random.randrange(100000, 999999)

    @staticmethod
    def create_contact_account(user_id):
        api_key = RAZORPAY_KEY_ID
        api_key_secret = RAZORPAY_KEY_SECRET
        request_url = RAZORPAY_CONTACT_ENDPOINT
        headers = {'x-api-key': api_key, 'x-api-secret': api_key_secret}
        #headers = {api_key: api_key_secret}

        user = User.objects.get(id=user_id)
        full_name = user.full_name
        contact = user.phone_num

        body = {
            'name': full_name,
            'contact': contact
        }

        response = requests.post(request_url, headers=headers, body=body)
        if response.status_code == 200:
            response_data = response.json()
            serializer = ContactSerializer(data=response_data)
            if serializer.is_valid():
                serializer.save()


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
