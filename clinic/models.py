from django.db import models

# Create your models here.

class Clinic(models.Model):
    name = models.TextField()
    profilePic = models.ImageField( blank=True)
    bio = models.TextField( blank=True)
    latitude = models.CharField(blank=True)
    longtitude = models.CharField(blank=True)
    

