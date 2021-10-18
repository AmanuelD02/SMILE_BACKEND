from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Address, Location, User, Verification, Link, Dentist


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['phone_num', 'code']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_num']



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','latitude','longtiude']



class AddressSerializer(serializers.ModelSerializer):
     class Meta:
        model = Address
        fields = ['id','country','city','state', 'street']




class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'




class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = '__all__'
