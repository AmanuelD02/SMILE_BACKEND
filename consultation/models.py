import uuid
from django.db import models
from users.models import User, Dentist
from treatment.models import Treatment
from payment.models import Wallet
import decimal
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from notification.models import Notification as Notify
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
# Create your models here.


class ConsultationRequest(models.Model):
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dentist_id', 'user_id'], name='ConsultationRequest')
        ]


class PendingConsultation(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        user = self.user_id
        wallet = Wallet.objects.filter(id=user_id).first()
        dentist = Dentist.objects.filter(id=dentist_id)
        if dentist and dentist.consultation_availabilty:
            price = wallet.balance - dentist.consultation_availabilty
            zero = decimal.Decimal(0)
            if c.compare(zero) == 1:
                return super().save()
            else:
                return ValueError("Low Balance")
        else:
            raise ValueError("Dentist Not Available")


class Consultation(models.Model):

    CONSULTATION_STATUS_OPEN = 'o'
    CONSULTATION_STATUS_CLOSE = 'c'
    CONSULTATION_STATUS_CHOICE = [
        (CONSULTATION_STATUS_OPEN, 'open'), (CONSULTATION_STATUS_CLOSE, 'close')]

    id = models.UUIDField(primary_key=True, null=False,
                          default=uuid.uuid4, editable=False)
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default=CONSULTATION_STATUS_OPEN)
    starting_time = models.DateTimeField(auto_now_add=True)
    ending_time = models.DateTimeField(blank=True)

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


class ConsultationMessage(models.Model):
    chat_id = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name='consultation_chat')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='consultation_sender')
    receiver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='consultation_receiver',)

    def previous_messages():
        return ConsultationMessage.objects.order_by('-created_at').all()


class ConsultationTask(models.Model):
    task_id = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    consultation_id = models.ForeignKey(Consultation, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['task_id', 'user_id', 'consultation_id'], name='ConsultationTask')
        ]


@receiver(post_save, sender=Consultation)
def notify_users(sender, instance, **kwargs):
    dentist = Dentist.objects.filter(id=instance.dentist_id)

    title = dentist.name
    body = "Consultation Chat Approved! Start Messaging"

    notification = Notify()
    notification.type = 'consultation'
    notification.content = body
    notification.sender_id = instance.dentist_id.id
    notification.reciever_id = instance.user_id
    notification.created_at = datetime.now()

    notification.save()
    reciever_id = instance.user_id
    FCMDevice.objects.filter(user_id=reciever_id).send_message(
        message=Message(notification=Notification(title=title, body=body)))
