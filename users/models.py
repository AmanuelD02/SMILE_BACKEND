from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    DENTIST_ROLE = 'D'
    PATIENT_ROLE = 'P'
    USER_ROLE_CHOICES = [(DENTIST_ROLE, 'Dentist'), (PATIENT_ROLE, 'Patient')]


    full_name = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=15, unique=True)
    # password = models.CharField(max_length=255)
    role = models.CharField(max_length=1, choices=USER_ROLE_CHOICES, default=DENTIST_ROLE)

    date_of_birth = models.DateField()
    bio = models.TextField()
    profile_pic_path = models.CharField()
    slug = models.SlugField()
    username = None
    password = None
    

    USERNAME_FIELD = 'phone_num'


class Verification(models.Model):
    phone_num = models.CharField(max_length=15, unique=True, primary_key=True)
    code = models.IntegerField(null=False)
    expiration_date = models.DateTimeField()







class Dentist(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    appointment_rate = models.FloatField()
    consultation_rate = models.FloatField()
    experience_year = models.PositiveIntegerField()
    document_path = models.CharField()
    verified = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField()
    consultation_availabilty = models.BooleanField(default=False)


class Location(models.Model):
    id = models.OneToOneField(Dentist, on_delete=models.CASCADE)
    latitude = models.CharField()
    longtiude = models.CharField()


class Address(models.Model):
    id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)


class Link(models.Model):
    id = models.ForeignKey(Dentist, on_delete=models.CASCADE )
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=255, blank=True)
    telegram = models.CharField(max_length=255, blank=True)


