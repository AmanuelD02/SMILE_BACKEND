from django.db import models
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from consultation.models import Consultation
import requests
import os
from dotenv import load_dotenv
from smile import celery
# Create your models here.

load_dotenv()
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
RAZORPAY_CONTACT_ENDPOINT = os.getenv('RAZORPAY_CONTACT_ENDPOINT')
RAZORPAY_FUND_ACCOUNT_ENDPOINT = os.getenv('RAZORPAY_FUND_ACCOUNT_ENDPOINT')
RAZORPAY_FUND_ACCOUNTS_BANK_ACCOUNT = os.getenv(
    'RAZORPAY_FUND_ACCOUNTS_BANK_ACCOUNT')


class Wallet(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=1000, decimal_places=2)


@receiver(pre_save, sender=Wallet)
def check_ongoing_chat_before_withdrawal(sender, instance, **kwargs):

    # Create the celery inspector to inspect all workers
    i = celery.app.control.inspect()
    scheduled_tasks = i.scheduled()
    consultation_id = 0
    if not scheduled_tasks:
        return 
    for task in scheduled_tasks:
        print(task)
        # Retrieve the task, update the time or terminate it
    user_id = instance.id
    user_consultation = Consultation.objects.filter(user_id=user_id)
    # There need to be guarantee that there is only one ongoing chat
    if user_consultation:
        if user_consultation.filter(status='open'):
            print()


class DepositTransaction(models.Model):
    TRANSACTION_TYPES = [('Deposit', 'Deposit'), ('WithDrawal', 'WithDrawal')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    payment_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    SERVICE_TREATMENT = 'Treatment'
    SERVICE_CONSULTATION = 'Consultation'
    SERVICE_APPOINTMENT = 'Appointment'

    SERVICE_TYPES = [(SERVICE_TREATMENT, 'Treatment'), (SERVICE_CONSULTATION,
                                                        'Consultation'), (SERVICE_APPOINTMENT, 'Appointment')]

    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_payer")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payment_reciever")
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    service_type = models.CharField(
        max_length=100, choices=SERVICE_TYPES, default=SERVICE_APPOINTMENT)
    service_date = models.DurationField(auto_created=True)


class Contact(models.Model):

    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contact_user")
    account_number = models.PositiveBigIntegerField(null=True, blank=True)
    contact_id = models.CharField(max_length=255)
    ifsc = models.CharField(blank=True, null=True, max_length=255)


class FundAccount(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_fund_account")
    fund_account = models.CharField(max_length=255)
    entity = models.CharField(max_length=255)
    is_active = models.BooleanField()
    account_type = models.CharField(max_length=255)


@receiver(post_save, sender=Contact)
def create_fund_account(sender, instance, **kwargs):
    """Function is called everytime a Contact is saved or updated. It checks whether the fund account already exists,
    and whether the updated Contact instance has the account_number and ifsc fields to save the new fund account"""

    # Check if the Fund Account already exists
    if FundAccount.objects.filter(user_id=instance.user_id).first():
        return
    # Check if the new Contact has account_number and ifsc
    if not instance.ifsc and not instance.account_number:
        return
    api_key = RAZORPAY_KEY_ID
    api_key_secret = RAZORPAY_KEY_SECRET
    request_url = RAZORPAY_CONTACT_ENDPOINT
    headers = {api_key: api_key_secret}

    full_name = ""
    user = User.objects.filter(id=instance.user_id).first()
    if user:
        full_name = user.full_name

    contact_id = instance.contact_id
    account_type = RAZORPAY_FUND_ACCOUNTS_BANK_ACCOUNT
    ifsc = instance.ifsc
    account_number = instance.account_number

    body = {
        "contact_id": contact_id,
        "account_type": account_type,
        "bank_account": {
            "name": full_name,
            "ifsc": ifsc,
            "account_number": account_number
        }
    }

    response = requests.post(request_url, headers=headers, body=body)
    if response.status_code == 200:
        response_data = response.json()
        fund_account_id = response_data['id']
        entity = response_data['entity']
        is_active = response_data['is_active']
        account_type = response_data['account_type']

        fund_account = FundAccount.objects.create(
            user_id=instance.user_id,
            fund_account=fund_account_id,
            entity=entity,
            is_active=is_active,
            account_type=account_type
        )
