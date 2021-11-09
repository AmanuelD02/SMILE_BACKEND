from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from payment.serializers import WalletSerializer, ContactSerializer

from .models import Wallet, Contact
# Create your views here.


class WalletView(APIView):
    def get(self, request, id):
        wallet = get_object_or_404(Wallet, pk=id)
        serializer = WalletSerializer(wallet)

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
