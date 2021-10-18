from django.db import models

from users.models import Dentist

# Create your models here.

class TreatmentName(models.Model):
    name = models.CharField(max_length=255)



class Treatment(models.Model):
    dentist_id = models.ForeignKey(Dentist,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    duration = models.TimeField()
    # check how to represent image 
    photo = models.CharField(blank= True,max_length=255)

