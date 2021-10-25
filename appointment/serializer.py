from django.db.models import fields
from rest_framework import serializers

from .models import Availability, PendingAppointment, AppointmentMessage


class AvailabiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['dentist_id', 'avaialble_at']


class PendingAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingAppointment
        fields = ['dentist_id', 'user_id', 'avaiable_at', 'treatment_id']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingAppointment
        fields = ['dentist_id', 'user_id', 'avaiable_at', 'treatment_id']
        read_only_fields = ['created_at']


class AppointmentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentMessage
        fields = ['chat_id', 'content',
                  'created_at', 'sender_id', 'reciever_id']
        read_only_fields = ['created_at']
