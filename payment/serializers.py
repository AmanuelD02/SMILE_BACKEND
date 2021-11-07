from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Wallet, Contact, FundAccount


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        models = Wallet
        fields = ['id', 'balance']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        models = Contact
        fields = ['user_id', 'account_number', 'contact_id', 'ifsc']
        read_only_fields = ['user_id', 'contact_id']


class FundAccountSerializer(serializers.ModelSerializer):
    class Meta:
        models = FundAccount
        fields = ['user_id', 'fund_account',
                  'entity', 'is_active', 'account_type']
