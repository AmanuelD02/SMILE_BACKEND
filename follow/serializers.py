
from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user_id','dentist_id','notification']
