import payment
from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, BaseUserManager
import requests
import os
from dotenv import load_dotenv

load_dotenv()
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_CONTACT_ENDPOINT = os.getenv('RAZORPAY_CONTACT_ENDPOINT')
RAZORPAY_FUND_ACCOUNT_ENDPOINT = os.getenv('RAZORPAY_FUND_ACCOUNT_ENDPOINT')


def upload_to(instance, filename):
    return '{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)


def upload_to_document(instance, filename):
    return 'document\{datetime}{filename}'.format(datetime=datetime.now(), filename=filename)


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_num, password=None, **extra_fields):
        """Create and save a User with the given phone_num and password."""
        if not phone_num:
            raise ValueError('The given phone_num must be set')

        user = self.model(phone_num=phone_num, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_num, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_num, password, **extra_fields)

    def create_superuser(self, phone_num, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone_num and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_num, password, **extra_fields)


class User(AbstractUser):
    DENTIST_ROLE = 'Dentist'
    PATIENT_ROLE = 'Patient'
    USER_ROLE_CHOICES = [(DENTIST_ROLE, 'D'), (PATIENT_ROLE, 'P')]

    full_name = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=15, unique=True)
    role = models.CharField(
        max_length=100, choices=USER_ROLE_CHOICES, default=PATIENT_ROLE)

    date_of_birth = models.DateField(null=True)
    bio = models.TextField(null=True)
    profile_pic = models.ImageField(
        upload_to=upload_to, default='media\default.png')
    # slug = models.SlugField(null=True)
    username = None
    # password = None

    USERNAME_FIELD = 'phone_num'
    objects = CustomUserManager()


@receiver(post_save, sender=User)
def create_contact_account(sender, instance, **kwargs):
    if payment.models.Contact.objects.filter(user_id=instance.id).first():
        return
    api_key = RAZORPAY_KEY_ID
    api_key_secret = RAZORPAY_KEY_SECRET
    request_url = RAZORPAY_CONTACT_ENDPOINT
    #headers = {'x-api-key': api_key, 'x-api-secret': api_key_secret}
    headers = {api_key: api_key_secret}

    user_id = instance.id
    full_name = instance.full_name
    contact = instance.phone_num

    body = {
        'name': full_name,
        'contact': contact
    }

    response = requests.post(request_url, headers=headers, body=body)
    if response.status_code == 200:
        response_data = response.json()
        contact_id = response_data['id']
        contact_account = payment.models.Contact.objects.create(
            user_id=user_id,
            contact_id=contact_id
        )


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
    document_path = models.FileField(blank=True, upload_to=upload_to_document)
    verified = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(blank=True,default=0)
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
