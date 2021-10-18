from django.db import models
from django.db.models.deletion import SET_DEFAULT
from users.models import User, Dentist 
from treatment.models import Treatment
# Create your models here.



class ConsultationRequest(models.Model):
    dentist_id = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dentist_id', 'user_id'], name='ConsultationRequest')
        ]


class Consultation(models.Model):
    CONSULTATION_STATUS_OPEN = 'o'
    CONSULTATION_STATUS_CLOSE = 'c'
    CONSULTATION_STATUS_CHOICE = [(CONSULTATION_STATUS_OPEN, 'open'),(CONSULTATION_STATUS_CLOSE, 'close')]

    dentist_id = models.ForeignKey(Dentist,on_delete=models.SET_DEFAULT)
    user_id = models.ForeignKey(User,on_delete=models.SET_DEFAULT)
    status = models.CharField(max_length=1, default=CONSULTATION_STATUS_OPEN)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField(blank=True)
    treatment_id = models.ForeignKey(Treatment,on_delete=models.SET_DEFAULT)     



class AppointmentMessage(models.Model):
    chat_id = models.ForeignKey(Consultation,on_delete=models.SET_DEFAULT)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(User,on_delete=models.SET_DEFAULT)
    reciever_id = models.ForeignKey(User,on_delete=models.SET_DEFAULT)


