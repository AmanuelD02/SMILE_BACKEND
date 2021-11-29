from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Address, Location, User, Verification, Link, Dentist
from fcm_django.models import FCMDevice
from drf_extra_fields.geo_fields import PointField

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['phone_num', 'code']


class UnauthorizedUserSerializer(serializers.Serializer):
    phone_num = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=255)
    registered = serializers.BooleanField()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_num', 'full_name', 'profile_pic', 'role','bio','date_of_birth')


class UserRegisterSerializer(serializers.ModelSerializer):
    # notification_id = serializers.CharField()
    class Meta:
        model = User
        fields = ('phone_num', 'full_name', 'profile_pic', 'role','bio','date_of_birth')
    # def create(self, validated_data):
    #     print("create method")
    #     print(validated_data)
    #     notification = validated_data.pop('notification_id') 
    #     print("validated and poped: \n")
        
    #     user = User.objects.create(**validated_data)
    #     user.save()
    #     print("create user object")
    #     return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'phone_num', 'profile_pic', 'role']


class UserEditSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    date_of_birth = serializers.DateField()
    bio = serializers.CharField(allow_blank=True)
    profile_pic = serializers.ImageField()


class LocationSerializer(serializers.ModelSerializer):
    location = PointField()
    class Meta:
        model = Location
        fields = ['id', 'location']


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
        read_only_fields = ['rating','verified']


class AllInformationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    link = LinkSerializer()
    address = AddressSerializer()
    class Meta:
        model= Dentist
        fields= ['id', 'clinic_name','degree','appointment_rate','consultation_rate',
        'experience_year','document_path','verified','rating',
        'consultation_availabilty', 'location','link','address',]



class SearchDentistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= User
        fields =['id','phone_num','profile_pic','bio','full_name']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        dentist = Dentist.objects.get(pk= instance.id)
        representation['dentist_info'] = DentistSerializer(dentist).data
        return representation


class TopDentistSerializer(serializers.ModelSerializer):
    class Meta:
        model= Dentist
        fields = '__all__'
        depth=2

class NearByDentistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Location
        fields =['id',]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        user = User.objects.get(pk=instance.id)

        representation['info'] = SearchDentistSerializer(user).data
        return representation
