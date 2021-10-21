from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


def upload_to(instance, filename):
    return 'media/{filename}'.format(filename=filename)


class User(AbstractUser):
    DENTIST_ROLE = 'D'
    PATIENT_ROLE = 'P'
    USER_ROLE_CHOICES = [(DENTIST_ROLE, 'Dentist'), (PATIENT_ROLE, 'Patient')]

    full_name = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=1, choices=USER_ROLE_CHOICES, default=DENTIST_ROLE)

    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    profile_pic = models.ImageField(
        upload_to=upload_to, default='media\default.png')
    slug = models.SlugField(null=True)
    username = None
    password = None

    USERNAME_FIELD = 'phone_num'


class Verification(models.Model):
    phone_num = models.CharField(max_length=15, unique=True, primary_key=True)
    code = models.IntegerField(null=False)
    expiration_date = models.DateTimeField()
    is_verified = models.BooleanField(default=False)


class Dentist(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    clinic_name = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    appointment_rate = models.FloatField()
    consultation_rate = models.FloatField()
    experience_year = models.PositiveIntegerField()
    document_path = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField()
    consultation_availabilty = models.BooleanField(default=False)


class Location(models.Model):
    id = models.OneToOneField(
        Dentist, on_delete=models.CASCADE, primary_key=True)
    latitude = models.CharField(max_length=255)
    longtiude = models.CharField(max_length=255)


class Address(models.Model):
    id = models.OneToOneField(
        Dentist, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)


class Link(models.Model):
    id = models.OneToOneField(
        Dentist, on_delete=models.CASCADE, primary_key=True)
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=255, blank=True)
    telegram = models.CharField(max_length=255, blank=True)
