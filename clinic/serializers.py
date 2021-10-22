from rest_framework import serializers
from .models import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'profile_pic', 'name', 'bio', 'latitude', 'longtitude']
