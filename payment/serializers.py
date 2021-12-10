from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import BankInfo, CardInfo, Wallet, Contact, FundAccount, Payment


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['user_id', 'account_number', 'contact_id', 'ifsc']
        read_only_fields = ['user_id', 'contact_id']


class FundAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundAccount
        fields = ['user_id', 'fund_account',
                  'account_type']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['receiver', 'amount', 'service_type']


class WithdrawBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance']
        read_only_fields = ['id']

class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = '__all__'


class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardInfo
        fields = '__all__'
