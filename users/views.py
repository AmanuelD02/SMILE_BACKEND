import os
import random
import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import Utils
from twilio.rest import Client
from dotenv import load_dotenv
from users.models import Verification, User
from twilio.rest import Client
from dotenv import load_dotenv
import datetime
from rest_framework import status, generics


from rest_framework_swagger import renderers
import jwt
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Address, Link, User, Dentist, Verification, Location
from .serializers import AddressSerializer, LinkSerializer, LocationSerializer, UserSerializer, DentistSerializer, UserRegisterSerializer, UnauthorizedUserSerializer, UserEditSerializer

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_ACCOUNT_TOKEN')
phone_number = os.getenv('TWILIO_PHONE_NUMBER')
EXPIRATION_INTERVAL = int(os.getenv('VERIFICATION_EXPIRATION_INTERVAL'))
SECRET_KEY = os.getenv('JWT_SECRET')

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny, ]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        data = request.data.dict()
        phone_num = data['phone_num']
        if User.objects.filter(phone_num=phone_num).first():
            return Response({"message": "Phone Number already used, please use a different one."},
                            status=status.HTTP_409_CONFLICT)
        serializer = UserRegisterSerializer(data=data)

        if serializer.is_valid():

            try:
                verification = Verification.objects.get(
                    phone_num=phone_num)
                if verification == None:
                    raise Verification.DoesNotExist
                serializer.save()
                user = User.objects.get(phone_num=phone_num)
                user_serializer = UserSerializer(user)
                token = Utils.encode_token(user)

                Verification.objects.filter(phone_num=phone_num).delete()
                return Response({"data": user_serializer.data, "token": token}, status=status.HTTP_201_CREATED)
            except Verification.DoesNotExist:
                return Response({
                    "message": "Please Verify Your Phone Number First"
                }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({
                "message": "Unsupported Data Type"
            }, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    permission_classes = [AllowAny, ]
    """
    User requests for authentication code by sending Phone Number
    """

    def post(self, request):

        client = Client(account_sid, auth_token)
        recipient_phone_number = request.data['phone_number']

        otp = generateOTP()

        try:
            verification = Verification.objects.get(
                phone_num=recipient_phone_number)
            verification.code = otp
            verification.expiration_date = timezone.now() + \
                datetime.timedelta(seconds=300)
            verification.save(update_fields=['code', 'expiration_date'])

        except Verification.DoesNotExist:
            verification = Verification.objects.create(
                code=otp,
                phone_num=recipient_phone_number,
                expiration_date=timezone.now() + datetime.timedelta(seconds=EXPIRATION_INTERVAL),
                is_verified=False,

            )

            verification.save()

        # body = f"Your Smile Verification code is {str(otp)}"
        # message = client.messages.create(
        #     from_=phone_number,
        #     body=body,
        #     to=recipient_phone_number
        # )

        # if message.sid:
        if otp:
            return Response({"message": f"Verification Code Sent"}, status=status.HTTP_201_CREATED)
        return Response("Error")


class AuthenticateOTPView(APIView):
    permission_classes = [AllowAny, ]
    """
    User sends Authentication code 
    """

    def post(self, request):
        data = {}
        phone_num = request.data['phone_num']
        code = request.data['code']
        verification = get_object_or_404(Verification, phone_num=phone_num)
        expiration_interval = datetime.timedelta(seconds=EXPIRATION_INTERVAL)
        if (verification.expiration_date - timezone.now() < expiration_interval):

            if verification.code == code:
                try:
                    user = User.objects.get(phone_num=phone_num)
                    if user == None:
                        raise AttributeError
                    token = Utils.encode_token(user)
                    serializer = UserSerializer(user)
                    data["message"] = "User Logged in"
                    data["phone_num"] = user.phone_num
                    user_serializer = UserSerializer(user)
                    response = {"data": user_serializer.data, "token": token}
                    Verification.objects.filter(phone_num=phone_num).delete()

                    return Response(response)

                except User.DoesNotExist:
                    message = "Please Register to Continue"
                    unauthorized_user_data = {
                        "phone_num": phone_num, "message": message}
                    unauthorized_user = UnauthorizedUserSerializer(
                        unauthorized_user_data).data

                    ##is_verified = true
                    Verification.objects.filter(
                        phone_num=phone_num).update(is_verified=True)
                    return Response(unauthorized_user)

        else:
            return Response({
                "message": "Verification Code Expired. Please try again."
            }, status=status.HTTP_400_BAD_REQUEST)


def generateOTP():

    return random.randrange(100000, 999999)


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        JWT_authenticator = JWTAuthentication()
        # Check and validate TOken from user
        # token = request.headers["Authorization"]
        user_id = ""
        request_data = request.data.dict()
        # try:
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            user, token = response
            user_id = user.id
        else:
            return Response({"message": "Invalid Token"})
        # print(decoded_token)
        # user_id = decoded_token['id']
        # print(user_id)
        #serializer = UserEditSerializer(data=request.data.dict())

        # except jwt.ExpiredSignatureError:
        #     return Response({"message": "Authentication Failed"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(id=user_id).first()
        if user != None:
            # if serializer.is_valid():
            user.full_name = request_data["full_name"]
            user.date_of_birth = request_data["date_of_birth"]
            user.bio = request_data["bio"]
            user.profile_pic = request_data["profile_pic"]
            user.save(update_fields=['full_name',
                      "date_of_birth", 'bio', 'profile_pic'])

            return Response({"Message": "Successfully Updated"})
            # else:
            #     return Response({"message": "Invalid Input"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Phone Number"}, status=status.HTTP_404_NOT_FOUND)


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
        location = get_object_or_404(Location, pk=request.data['id'])

        serializer = LocationSerializer(location, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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

    def put(self, request, id):
        address = get_object_or_404(Address, pk=request.data['id'])

        serializer = AddressSerializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        print("DELETE")
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

    def put(self, request, id):
        link = get_object_or_404(Link, pk=request.data['id'])

        serializer = LinkSerializer(link, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        dentist = get_object_or_404(Dentist, pk=id)
        serializer = DentistSerializer(dentist)

        return Response(serializer.data)

    def put(self, request, id):
        dentist = get_object_or_404(Dentist, pk=request.data['id'])

        serializer = DentistSerializer(dentist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        dentist = get_object_or_404(Dentist, pk=id)
        dentist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DentistView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        serializer = DentistSerializer(data=request.data.dict())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
