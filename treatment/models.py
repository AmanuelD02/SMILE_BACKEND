from django.db import models

from users.models import Dentist
from datetime import datetime
# Create your models here.


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)


class TreatmentName(models.Model):
    name = models.CharField(max_length=255)


class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(
        Dentist, on_delete=models.CASCADE, unique=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    duration = models.TimeField()
    photo = models.ImageField(
        upload_to=upload_to, default='medical\medical_service.png')
