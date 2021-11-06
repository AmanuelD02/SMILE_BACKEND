from enum import unique
from django.db import models
from users.models import User, Dentist
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.


class Review(models.Model):
    dentist_id = models.ForeignKey(
        Dentist, on_delete=models.CASCADE, related_name="Dentist")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=1, validators=[
                                 MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dentist_id', 'user_id'], name='Review')
        ]

@receiver(post_save, sender=Review)
def calculate_review(sender, instance, **kwargs):
    total = Review.objects.filter(dentist_id = instance.dentist_id).count()
    id = instance.dentist_id.id
    dentist = Dentist.objects.filter(id = id).first()
    rating =  ((dentist.rating * (total-1)) +instance.rating) / total
    dentist.rating =rating
    dentist.save()


@receiver(post_delete, sender=Review)
def calculate_review_delete(sender, instance, **kwargs):
    
    total = Review.objects.filter(dentist_id = instance.dentist_id).count()
    id = instance.dentist_id.id
    dentist = Dentist.objects.filter(id = id).first()
    if total ==0:
        dentist.rating = 0
        dentist.save()
    else:
        
        rating =  ((dentist.rating * (total+1)) - instance.rating) / total
        dentist.rating =rating
        dentist.save()

class ReviewLike(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['review_id', 'user_id'], name='ReviewLike')
        ]
