import decimal
import os
import json 

import requests
from dotenv import load_dotenv

from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from payment.serializers import BankInfoSerializer, FundAccountSerializer, WalletSerializer, ContactSerializer, PaymentSerializer, WithdrawBalanceSerializer

from .models import BankInfo, FundAccount, Wallet, Contact
# Create your views here.



load_dotenv()
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_CONTACT_ENDPOINT = os.getenv('RAZORPAY_CONTACT_ENDPOINT')
RAZORPAY_FUND_ACCOUNT_ENDPOINT = os.getenv('RAZORPAY_FUND_ACCOUNT_ENDPOINT')
RAZORPAY_FUND_ACCOUNTS_BANK_ACCOUNT = os.getenv(
    'RAZORPAY_FUND_ACCOUNTS_BANK_ACCOUNT')


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)
        if authentication is not None:
            user, token = authentication
            user_id = user.id

        wallet = get_object_or_404(Wallet, pk=user_id)
        serializer = WalletSerializer(wallet)

        return Response(serializer.data)

    def put(self, request):
        """
        This method should be used for depositing to wallet and asummes the amount is valid amount
        """

        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)
        if authentication is not None:
            user, token = authentication
            user_id = user.id

        wallet = get_object_or_404(Wallet, pk=user_id)
        amount = request.data['amount']

        wallet.balance += decimal.Decimal(amount)
        wallet.save()
        serializer = WalletSerializer(wallet)

        # SEND NOTIFICATION
        FCMDevice.objects.filter(user_id=user_id).send_message(message=Message(notification=Notification(
            title="Transaction Completed", body=f'you have succesfully Deposited  {amount}')))

        # SEND NOTIFICATION
        return Response(serializer.data)


class UpdateContact(APIView):
    """
    Class to update the Razorpay Contact
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)
        if authentication is not None:
            user, token = authentication
            user_id = user.id

            contact_account = get_object_or_404(Contact, pk=user_id)
            serializer = ContactSerializer(contact_account, data=request.data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"message": "Unsupported Data Type"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Unauthorized Access"}, status=status.HTTP_401_UNAUTHORIZED)


class PerformPayment(APIView):
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)
        if authentication is not None:
            user, token = authentication
            user_id = user.id

            serializer = PaymentSerializer(data=request.data)
            user_balance = Wallet.objects.get(id=user_id)
            amount = decimal.Decimal(serializer.data['amount'])
            receiver_balance = Wallet.objects.get(
                id=serializer.data['receiver'])
            if user_balance > amount:
                return Response({"message": "You don't have enough money."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_balance.balance -= amount
                receiver_balance.balance += amount
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Unauthorized Access"}, status=status.HTTP_401_UNAUTHORIZED)


class WithdrawBalance(APIView):
    def post(self, request):
        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)

        if authentication is not None:
            user, token = authentication
            user_id = user.id


class BankInfoDetailView(APIView):
    def get(self, request, id):
        bank = get_object_or_404(BankInfo, pk=id)
        serializer = BankInfoSerializer(bank)

        return Response(serializer.data)


class FundAccountView(APIView):
    def get(self,request, id):
        funds = get_object_or_404(FundAccount, pk=id)

        serializer = FundAccountSerializer(funds,many=True)

        return Response(serializer.data)
        
class BankInfoView(APIView):

    def post(self, request):
        from users.models import User
        JWT_authenticator = JWTAuthentication()
        authentication = JWT_authenticator.authenticate(request)
        user, token = authentication
        user_id = user.id
        bank = BankInfo.objects.filter(id= user_id).first()
        if bank:
            bank.delete()

        serializer = BankInfoSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        a = serializer.validated_data['id'].id
        if user_id != serializer.validated_data['id'].id:
            return Response({"message":"Unauthorized Access"}, status= status.HTTP_401_UNAUTHORIZED)

        fund = FundAccount.objects.filter(user_id= user_id).filter(account_type= 'bank_account').first()
        contact = Contact.objects.filter(user_id = user_id).first()
        user = User.objects.filter(id = user_id).first()
        if fund:
            fund.delete()

        serializer.save()
        api_key = RAZORPAY_KEY_ID
        api_key_secret = RAZORPAY_KEY_SECRET
        request_url = RAZORPAY_FUND_ACCOUNT_ENDPOINT

        body = {
         "contact_id": str(contact.contact_id),
         "account_type": "bank_account",
         "bank_account" : {
             "name": user.full_name,
             "ifsc": bank.ifsc,
             "account_number": bank.account_number
                    },
             }
        json_dump = json.dumps(body)

        print(json_dump)
        response = requests.post(request_url, auth=(api_key, api_key_secret), data=json_dump)

        print(response.json())
        if response.status_code == 200:
            response_data = response.json()
            fund_account_id = response_data['id']
            fund = FundAccount()
            fund.user_id = user_id
            fund.account_type = 'bank_account'
            fund.fund_account = fund_account_id

            fund.save()

            return Response({"message":"Succesfully added Bank Information"})
        else:
            return Response(response.json(),status=status.HTTP_400_BAD_REQUEST)
    