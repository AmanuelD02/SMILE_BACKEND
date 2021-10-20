import os
import random
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
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




## ADD DENTIST DETAIL

### DENTIST LOCATION
class LocationView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    
class LocationDetailView(APIView):
    def get(self, request, id):
        location = get_object_or_404(Location, pk= id)
        serializer = LocationSerializer(location)

        return Response(serializer.data)

    def put(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        location = get_object_or_404(Location, pk= id)
        location.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
##
## END OF DENTIST LOCATION
##


##
## DENTIST ADDRESS
##
class AddressView(APIView):
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



class AddressDetailView(APIView):
    def get(self, request, id):
        address = get_object_or_404(Address, pk= id)
        serializer = AddressSerializer(address)

        return Response(serializer.data)

    def put(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        address = get_object_or_404(Address, pk= id)
        address.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

##
## END OF DENTIST ADDRESS
##


##
## Dentist Link
##


class LinkView(APIView):
    def post(self, request):
        serializer = LinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class LinkDetailView(APIView):
    def get(self, request, id):
        link = get_object_or_404(Link, pk= id)
        serializer = LinkSerializer(link)

        return Response(serializer.data)

    def put(self, request):
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        link = get_object_or_404(Link, pk= id)
        link.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

##
## END Of Dentist Link
##



##
##  Dentist INFO
##
class DentistDetailView(APIView):
    def get(self, request, id):
        dentist = get_object_or_404(Dentist, pk= id)
        serializer = DentistSerializer(dentist)

        return Response(serializer.data)

    def put(self, request):
        serializer = DentistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        dentist = get_object_or_404(Dentist, pk= id)
        dentist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DentistView(APIView):
    def post(self, request):
        serializer = DentistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)