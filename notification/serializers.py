from django.db import models
from django.db.models import fields
from rest_framework import serializers


from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        models = Notification
        fields = ['id','type', 'content', 'created_at', 'sender_id', 'reciever_id','is_seen']
        read_only_fields = ['id', 'created_at']
        