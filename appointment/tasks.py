from datetime import datetime
from celery import shared_task

from .models import Availability, PendingAppointment


@shared_task
def delete_expired_availablity_and_pending_appointment():
    available = Availability.objects.filter(available_at__lt=datetime.now())
    available.delete() 

    pending = PendingAppointment.objects.filter(available_at__lt=datetime.now())
    pending.delete()
