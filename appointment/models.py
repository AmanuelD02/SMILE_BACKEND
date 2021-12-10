from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notification.models import Notification as Notify
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from payment.models import Wallet
import decimal

from users.models import User, Dentist
from treatment.models import Treatment

# Create your models here.


class Availability(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    available_at = models.DateTimeField(unique=True)


class PendingAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        user = self.user_id
        wallet = Wallet.objects.filter(id=user.id).first()
        treatment = self.treatment_id
        c = wallet.balance - treatment.price
        zero = decimal.Decimal(0)
        r = c.compare(zero)

        if c.compare(zero) == 1:
            return super().save()
        else:
            return


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        user = self.user_id
        wallet = Wallet.objects.filter(id=user.id).first()
        treatment = self.treatment_id
        c = wallet.balance - treatment.price
        zero = decimal.Decimal(0)
        r = c.compare(zero)

        if c.compare(zero) == 1:
            wallet.balance = c
            wallet.save()
            r = wallet.balance

            return super().save()
        else:
            raise ValueError("Low Balance")


class AppointmentChat(models.Model):
    PRE_APPOINTMENT = 'pre'
    POST_APPOINTMENT = 'post'
    STATUS = [(PRE_APPOINTMENT, PRE_APPOINTMENT),
              (POST_APPOINTMENT, POST_APPOINTMENT)]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=STATUS, default=PRE_APPOINTMENT)
    expiration_date = models.DateTimeField()


class AppointmentMessage(models.Model):
    chat_id = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='appointment_chat')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointment_sender")
    reciever_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointment_reciever")


@receiver(post_save, sender=Appointment)
def notify_users(sender, instance, **kwargs):
    # notify users here
    title = "Appointment"
    body = "Appointment Approved!"

    notification = Notify()
    notification.type = 'appointment'
    notification.content = body
    notification.sender_id = instance.dentist_id.id
    notification.reciever_id = instance.user_id
    notification.created_at = datetime.now()

    notification.save()

    reciever_id = instance.user_id
    FCMDevice.objects.filter(user_id=reciever_id).send_message(
        message=Message(notification=Notification(title=title, body=body)))
    # FCMDevice.objects.all().send_message(message:Message(Notification(title="Appointment success",body="The Densitst dentist_id has approved ur appointment")))


@receiver(post_save, sender=Appointment)
def delete_pending_appointments(sender, instance, **kwargs):
    appointment_date = instance.available_at
    pending = PendingAppointment.objects.filter(available_at=appointment_date)
    pending.delete()


@receiver(post_save, sender=Appointment)
def create_appointment_chat(sender, instance, **kwargs):
    chat = AppointmentChat()
    chat.user_id = instance.user_id
    chat.dentist_id = instance.dentist_id
    chat.appointment_id = instance
    chat.created_at = timezone.now()
    a = timezone.now() + timedelta(days=1)
    chat.expiration_date = timezone.now() + timedelta(days=1)
    chat.save()
