from django.db import models

from users.models import Dentist

# Create your models here.

class TreatmentName(models.Model):
    name = models.CharField()



class Treatment(models.Model):
    dentist_id = models.ForeignKey(Dentist,on_delete=models.CASCADE)
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField()
    duration = models.TimeField()
    # check how to represent image 
    photo = models.ImageField(blank= True)

