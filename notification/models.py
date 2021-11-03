from django.db import models
from django.db.models import Q

from  users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from fcm_django.models import FCMDevice

from firebase_admin.messaging import Message, Notification
# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPES = [('payment','payment'), ('review','review'), ('update_profile','update_profile'), ('appointment', 'appointment')]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender') 
    reciever_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_reciever')
    is_seen = models.BooleanField(default=False) 




# @receiver(post_save, sender=Notification)
# def notify_users(sender, instance: Notification, **kwargs):
#     # notify users here
#     title = instance.type
#     body =  instance.content
#     reciever_id = instance.reciever_id
#     sender_id = instance.sender_id


#     FCMDevice.objects.filter(Q(user_id = reciever_id) | Q(user_id = sender_id)).send_message(message=Message(notification=Notification(title=title, body=body)))
#         # FCMDevice.objects.all().send_message(message:Message(Notification(title="Appointment success",body="The Densitst dentist_id has approved ur appointment")))
    