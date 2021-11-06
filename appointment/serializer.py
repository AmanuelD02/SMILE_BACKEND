from django.db.models import fields
from rest_framework import serializers

from .models import Appointment, Availability, PendingAppointment, AppointmentMessage
from users.models import User

class AvailabiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'dentist_id', 'available_at']
        read_only_fields = ['id']


class PendingAppointmentSerializer(serializers.ModelSerializer):
    available_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = PendingAppointment
        fields = ['id', 'dentist_id', 'user_id',
                  'available_at',  'treatment_id']
        read_only_fields = ['id']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'dentist_id', 'user_id',
                  'available_at', 'treatment_id']
        read_only_fields = ['id']


class AppointmentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentMessage
        fields = ['id', 'chat_id', 'content',
                  'created_at', 'sender_id', 'reciever_id']
        read_only_fields = ['created_at', 'id']



class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Appointment
        fields = ['id','user_id','available_at','treatment_id']
        depth =2
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        del representation['user_id']['password']
        del representation['user_id']['last_login']
        del representation['user_id']['is_superuser']
        del representation['user_id']['groups']
        del representation['user_id']['user_permissions']
        del representation['user_id']['first_name']
        del representation['user_id']['last_name']
        del representation['user_id']['email']
        del representation['user_id']['is_staff']
        del representation['user_id']['is_active']
        return representation