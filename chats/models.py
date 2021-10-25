from django.db import models
from users.models import User
# Create your models here.


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField()
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField()
