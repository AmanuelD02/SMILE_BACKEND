from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


from payment.serializers import WalletSerializer

from .models import Wallet
# Create your views here.


class WalletView(APIView):
    def get(self, request, id):
        wallet = get_object_or_404(Wallet, pk=id)
        serializer = WalletSerializer(wallet)
        
        
        return Response(serializer.data)

