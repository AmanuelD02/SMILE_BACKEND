import jwt
import os
import datetime
import json
from dotenv import load_dotenv

from django.shortcuts import get_object_or_404
from django.utils import timezone

from dotenv import load_dotenv
from twilio.rest import Client


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_swagger import renderers
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Verification, User
from .utils import Utils

from .models import Address, Link, User, Dentist, Verification, Location
from .serializers import AddressSerializer, AllInformationSerializer, LinkSerializer, LocationSerializer, SearchDentistSerializer, UserSerializer, DentistSerializer, UserRegisterSerializer, UnauthorizedUserSerializer, UserEditSerializer

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

                # Delete the verification information from the verification table
                Verification.objects.filter(phone_num=phone_num).delete()

                # create a contact model for the user

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

        otp = Utils.generateOTP()

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
        #     twilio_response = json.loads(message.sid)
        #     if twilio_response['status'] == 'sent':
        #         return Response({"message": f"Verification Code Sent"}, status=status.HTTP_201_CREATED)

        #     # If twilio responds with "Invalid Phone Number" error
        #     elif int(twilio_response['error_code']) == 60033:
        #         return Response({"message": twilio_response['error_message']}, status=status.HTTP_400_BAD_REQUEST)
        if otp:
            return Response({"message": f"Verification Code Sent {str(otp)}"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateOTPView(APIView):
    permission_classes = [AllowAny, ]
    """
    User sends Authentication code 
    """

    def post(self, request):
        data = {}
        phone_num = request.data['phone_num']
        code = request.data['code']
        # device_id = request.data['device_id']
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
                    response = {"data": user_serializer.data,
                                "token": token, "registered": True}
                    Verification.objects.filter(phone_num=phone_num).delete()

                    return Response(response, status=status.HTTP_200_OK)

                except User.DoesNotExist:
                    message = "Please Register to Continue"
                    unauthorized_user_data = {
                        "phone_num": phone_num, "message": message, "registered": False}
                    unauthorized_user = UnauthorizedUserSerializer(
                        unauthorized_user_data).data

                    ##is_verified = true
                    Verification.objects.filter(
                        phone_num=phone_num).update(is_verified=True)
                    return Response(unauthorized_user, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Incorrect Verification Code."
                }, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response({
                "message": "Verification Code Expired. Please try again."
            }, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class EditProfileView(APIView):
    """
    A view for user to edit profile. Authentication is required
    """
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
            return Response({"message": "Invalid Authorization Token"}, status=status.HTTP_401_UNAUTHORIZED)
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

            return Response({"Message": "Successfully Updated"}, status=status.HTTP_200_OK)
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


class DentistAllInfoView(APIView):
    def get(self, request, id):
        user = get_object_or_404(Dentist, pk=id)
        serializer = AllInformationSerializer(user)

        return Response(serializer.data)


class SearchDentistListView(ListAPIView):
    serializer_class = SearchDentistSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        name = self.request.query_params.get('full_name')
        queryset = User.objects.filter(full_name__contains=name)
        return queryset