from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Address, Location, User, Verification, Link, Dentist


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['phone_num', 'code']


class UnauthorizedUserSerializer(serializers.Serializer):
    phone_num = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=255)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_num', 'full_name', 'profile_pic', 'role')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_num']


class UserEditSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    bio = serializers.CharField(allow_blank=True)
    profile_pic = serializers.ImageField()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longtiude']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'country', 'city', 'state', 'street']


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'
