from django.db.models import fields
from rest_framework import serializers
from .models import User, Verification


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['phone_num', 'code']


class UnauthorizedUserSerializer(serializers.Serializer):
    phone_num = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_num']


#serializer = UnauthorizedUserSerializer()
