from django.db.models import fields
from rest_framework import serializers
from .models import User, Verification


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['phone_num', 'code']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_num']
