from enum import unique
from django.db import models
from users.models import User, Dentist
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Review(models.Model):
    dentist_id= models.ForeignKey(Dentist,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dentist_id', 'user_id'], name='Review')
        ]


class ReviewLike(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['review_id', 'user_id'], name='ReviewLike')
        ]
