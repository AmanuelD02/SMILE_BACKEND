from django.db import models
from users.models import User, Dentist
# Create your models here.

class Follow(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'dentist_id'], name='Follow')
        ]
