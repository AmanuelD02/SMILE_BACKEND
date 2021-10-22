from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Treatment, TreatmentName


class TreatmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= TreatmentName
        fields= ['id', 'name']
        read_only_fields = ['id']


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id','dentist_id', 'name','description', 'price', 'duration', 'photo']
        read_only_fields = ['id']
