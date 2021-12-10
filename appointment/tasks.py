from datetime import datetime
from celery import shared_task

from .models import Availability, PendingAppointment
from appointment.utils import end_appointment_chat


@shared_task
def delete_expired_availablity_and_pending_appointment():
    print("DELETE Expired ")
    available = Availability.objects.filter(available_at__lt=datetime.now())
    available.delete()

    pending = PendingAppointment.objects.filter(
        available_at__lt=datetime.now())
    pending.delete()


@shared_task
def terminate_appointment_chat(appointment_chat_id):
    end_appointment_chat(appointment_chat_id)
