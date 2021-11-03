from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        models = Wallet
        fields = ['id', 'balance']

        