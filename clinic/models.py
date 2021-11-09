from django.db import models
from datetime import datetime
# Create your models here.


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)


class Clinic(models.Model):
    name = models.TextField()
    profile_pic = models.ImageField(
        upload_to=upload_to, default='media\clinic_default.png')
    bio = models.TextField(blank=True)
    latitude = models.CharField(blank=True, max_length=255)
    longtitude = models.CharField(blank=True, max_length=255)
