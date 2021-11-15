# from django.db import models
from datetime import datetime
from django.contrib.gis.db import models

# Create your models here.


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)


class Clinic(models.Model):
    name = models.TextField()
    profile_pic = models.ImageField(
        upload_to=upload_to, default='media\clinic_default.png')
    bio = models.TextField(blank=True)
    location = models.PointField(srid=4326,blank=True)

