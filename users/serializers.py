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


#serializer = UnauthorizedUserSerializer()

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
