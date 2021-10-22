from django.db import models
from users.models import User
# Create your models here.

class Wallet(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=1000, decimal_places=2)



class Payment(models.Model):
    SERVICE_TREATMENT = 'T'
    SERVICE_CONSULTATION = 'C'
    SERVICE_APPOINTMENT = 'A'


    SERVICE_TYPES= [(SERVICE_TREATMENT, 'Treatment'), (SERVICE_CONSULTATION, 'Consultation'), (SERVICE_APPOINTMENT, 'Appointment')]

    payer = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="payment_payer")
    reciever =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_reciever")
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    service_type = models.CharField(max_length=1, choices=SERVICE_TYPES, default=SERVICE_APPOINTMENT)
    service_date = models.DurationField(auto_created=True)

