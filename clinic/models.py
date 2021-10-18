from django.db import models

# Create your models here.

class Clinic(models.Model):
    name = models.TextField()
    profilePic = models.CharField( blank=True,max_length=255)
    bio = models.TextField( blank=True)
    latitude = models.CharField(blank=True,max_length=255)
    longtitude = models.CharField(blank=True,max_length=255)
    

