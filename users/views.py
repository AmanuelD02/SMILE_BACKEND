import os
import random
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, UnauthorizedUserSerializer
from twilio.rest import Client
from dotenv import load_dotenv
from users.models import Verification, User
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status


from .models import Address, Link, User, Dentist, Verification, Location
from .serializers import AddressSerializer, LinkSerializer, LocationSerializer, UserSerializer, DentistSerializer

# Create your views here.
load_dotenv()


class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_num']
            if Verification.objects.get(phone_num=phone_number).is_verified == True:
                serializer.save()
            else:
                return Response({
                    "message": "Please Verify Your Phone Number First"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendOTPView(APIView):
    """
    User requests for authentication code by sending Phone Number
    """

    def post(self, request):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_ACCOUNT_TOKEN')
        phone_number = os.getenv('TWILIO_PHONE_NUMBER')

        client = Client(account_sid, auth_token)
        recipient_phone_number = request.data['phone_number']

        otp = generateOTP()

        try:
            verification = Verification.objects.get(phone_num=phone_number)
            verification.code = otp
            verification.expiration_date = datetime.now() + timedelta(seconds=300)
            verification.save()

        except:
            verification = Verification.objects.create(
                code=otp,
                phone_num=recipient_phone_number,
                expiration_date=datetime.now() + timedelta(seconds=300),
                is_verified=False
            )

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


class AuthenticateOTPView(APIView):
    """
    User sends Authentication code 
    """

    def post(self, request):
        data = {}
        phone_num = request.data['phone_number']
        code = request.data['code']
        verification = get_object_or_404(Verification, phone_num=phone_num)

        if (datetime.now() <= expiration_interval):
            if verification.code == code:
                try:

                    user = User.objects.get(phone_num=phone_num)
                    token = Token.objects.create(user=user)
                    serializer = UserSerializer(user)
                    data["message"] = "User Logged in"
                    data["phone_number"] = user.phone_num
                    response = {"data": data, "token": token}

                    return Response(response)

                except User.DoesNotExist:
                    message = "Please Register to Continue"
                    unauthorized_user_data = {
                        "phone_number": phone_num, "message": message}
                    unauthorized_user = UnauthorizedUserSerializer(
                        unauthorized_user_data).data
                    return Response(unauthorized_user)

                finally:
                    # Delete the code from verification Table
                    Verification.objects.delete(phone_num=phone_num)

        else:
            return Response({
                "message": "Verification Code Expired. Please try again."
            }, status=status.HTTP_400_BAD_REQUEST)


def generateOTP():

    return random.randrange(100000, 999999)


# ADD DENTIST DETAIL

# DENTIST LOCATION
class LocationView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LocationDetailView(APIView):
    def get(self, request, id):
        location = get_object_or_404(Location, pk=id)
        serializer = LocationSerializer(location)

        return Response(serializer.data)

    def put(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        location = get_object_or_404(Location, pk=id)
        location.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

##
# END OF DENTIST LOCATION
##


##
# DENTIST ADDRESS
##
class AddressView(APIView):
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class AddressDetailView(APIView):
    def get(self, request, id):
        address = get_object_or_404(Address, pk=id)
        serializer = AddressSerializer(address)

        return Response(serializer.data)

    def put(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        address = get_object_or_404(Address, pk=id)
        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

##
# END OF DENTIST ADDRESS
##


##
# Dentist Link
##


class LinkView(APIView):
    def post(self, request):
        serializer = LinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LinkDetailView(APIView):
    def get(self, request, id):
        link = get_object_or_404(Link, pk=id)
        serializer = LinkSerializer(link)

        return Response(serializer.data)

    def put(self, request):
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        link = get_object_or_404(Link, pk=id)
        link.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

##
# END Of Dentist Link
##


##
# Dentist INFO
##
class DentistDetailView(APIView):
    def get(self, request, id):
        dentist = get_object_or_404(Dentist, pk=id)
        serializer = DentistSerializer(dentist)

        return Response(serializer.data)

    def put(self, request):
        serializer = DentistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        dentist = get_object_or_404(Dentist, pk=id)
        dentist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DentistView(APIView):
    def post(self, request):
        serializer = DentistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
