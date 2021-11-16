import decimal
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from payment.serializers import WalletSerializer, ContactSerializer, PaymentSerializer, WithdrawBalanceSerializer

from .models import Wallet, Contact
# Create your views here.


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
