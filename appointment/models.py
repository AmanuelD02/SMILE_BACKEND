from django.db import models

from users.models import User, Dentist
from treatment.models import Treatment


from django.db.models.signals import post_save
from django.dispatch import receiver


from fcm_django.models import FCMDevice

from firebase_admin.messaging import Message, Notification
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


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


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

    reciever_id = instance.user_id
    FCMDevice.objects.filter(user_id = reciever_id).send_message(message=Message(notification=Notification(title=title, body=body)))
        # FCMDevice.objects.all().send_message(message:Message(Notification(title="Appointment success",body="The Densitst dentist_id has approved ur appointment")))
    