from users.models import Dentist, User
from appointment.models import Appointment
from channels.db import database_sync_to_async
from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@database_sync_to_async
def get_appointment(appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.status == 'close':
            return None
        return appointment
    except Appointment.DoesNotExist:
        return None


@database_sync_to_async
def verify_appointment_user(appointment, user):
    """Verifies if a user belongs to a chat """
    """Make Sure to give the function non-null data"""

    if appointment.user_id == user.id or appointment.dentist_id == user.id:
        return True
    else:
        return False


def end_appointment_chat(appointment_id):
    data = {
        "type": "disconnect",
        "message": "This Appointment Chat has been terminated",
        "appointment_id": appointment_id
    }
    room_name = f'chat_{appointment_id}'
    async_to_sync(channel_layer.send)(room_name, data)
