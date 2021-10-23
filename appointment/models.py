from django.db import models

from users.models import User, Dentist 
from treatment.models import Treatment
# Create your models here.


class Availability(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist,on_delete=models.CASCADE)
    available_at = models.DateTimeField()



class PendingAppointment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    treatment_id = models.ForeignKey(Treatment,on_delete=models.CASCADE)     



class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    dentist_id = models.ForeignKey(Dentist,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    treatment_id = models.ForeignKey(Treatment,on_delete=models.CASCADE)     



class AppointmentMessage(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name='appointment_chat')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="appointment_sender")
    reciever_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="appointment_reciever")





