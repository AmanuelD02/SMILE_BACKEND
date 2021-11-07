from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Review, ReviewLike


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','dentist_id', 'user_id', 'content', 'rating']
        read_only_fields= ['id']


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = ['review_id', 'user_id']
        depth=2
    

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
