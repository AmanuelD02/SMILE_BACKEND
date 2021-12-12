from django.db.models import fields
from rest_framework import serializers
from consultation.models import PendingConsultation, Consultation, ConsultationMessage
from users.models import Dentist, User


class PendingConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingConsultation
        fields = ['id', 'dentist_id', 'user_id','duration']
        read_only_fields = ['id']


class ConsultationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationMessage
        fields = ['id', 'chat_id', 'content',
                  'created_at', 'sender_id', 'receiver_id']
        read_only_fields = ['created_at', 'id']


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'dentist_id', 'user_id',
                  'status', 'starting_time', 'ending_time']
        
        read_only_fields = ['id','status','starting_time','ending_time']

