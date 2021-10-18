import os
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from twilio.rest import Client
from dotenv import load_dotenv
from users.models import Verification
from datetime import datetime, timedelta

# Create your views here.
load_dotenv()


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)


class SendOTPView(APIView):
    def post(self, request):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_ACCOUNT_TOKEN')
        phone_number = os.getenv('TWILIO_PHONE_NUMBER')

        client = Client(account_sid, auth_token)
        recipient_phone_number = request.data['phone_number']

        otp = generateOTP()
        if(Verification(phone_number=recipient_phone_number) == None):
            verification = Verification()

            verification.code = otp
            verification.phone_num = recipient_phone_number
            verification.expiration_date = datetime.now() + timedelta(seconds=300)

            verification.save()
        else:
            verification = Verification(phone_number=recipient_phone_number)
            verification.code = otp
            verification.expiration_date = datetime.now() + timedelta(seconds=300)

            verification.save()

        body = f"Your Smile Verification code is {str(otp)}"
        message = client.messages.create(
            from_=phone_number,
            body=body,
            to=recipient_phone_number
        )

        if message.sid:
            return Response('ok')
        return Response("Error")


def generateOTP():

    return random.randrange(100000, 999999)
