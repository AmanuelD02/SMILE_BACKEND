from rest_framework import serializers
from .models import Clinic
from drf_extra_fields.geo_fields import PointField


class ClinicSerializer(serializers.ModelSerializer):
    location = PointField()
    class Meta:
        model = Clinic
        fields = ['id', 'profile_pic', 'name', 'bio', 'location']
