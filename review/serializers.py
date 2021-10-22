from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Review, ReviewLike


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['dentist_id', 'user_id', 'content', 'rating']


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = ['review_id', 'user_id']
