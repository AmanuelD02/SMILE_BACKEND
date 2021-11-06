from django.db import models
from users.models import User
# Create your models here.

class Wallet(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=1000, decimal_places=2)



class DepositTransaction(models.Model):
    TRANSACTION_TYPES = [('Deposit','Deposit'), ('WithDrawal','WithDrawal')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)



class Payment(models.Model):
    SERVICE_TREATMENT = 'Treatment'
    SERVICE_CONSULTATION = 'Consultation'
    SERVICE_APPOINTMENT = 'Appointment'


    SERVICE_TYPES= [(SERVICE_TREATMENT, 'Treatment'), (SERVICE_CONSULTATION, 'Consultation'), (SERVICE_APPOINTMENT, 'Appointment')]

    payer = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="payment_payer")
    reciever =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_reciever")
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPES, default=SERVICE_APPOINTMENT)
    service_date = models.DurationField(auto_created=True)

