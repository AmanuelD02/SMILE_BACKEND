from users.models import Dentist, User
from .models import Consultation, ConsultationRequest
from channels.db import database_sync_to_async
from payment.models import Wallet
from datetime import timedelta
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@database_sync_to_async
def get_user(decoded_token):

    try:
        return User.objects.get(id=decoded_token['id'])
    except User.DoesNotExist:
        return None


@database_sync_to_async
def get_consultation(consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        if consultation.status == 'close':
            return None
        return consultation
    except Consultation.DoesNotExist:
        return None


@database_sync_to_async
def verify_consultation_user(consultation, user):
    """Verifies if a user belongs to a chat """
    """Make Sure to give the function non-null data"""

    if consultation.user_id == user.id or consultation.dentist_id == user.id:
        return True
    else:
        return False


@database_sync_to_async
def get_user_wallet(user_id):
    """Retrieve User Balance from the wallet"""

    try:
        return Wallet.objects.get(id=user_id)
    except Wallet.DoesNotExist:
        return None


@database_sync_to_async
def check_user_balance(wallet, consultation_id):
    """Check the balance of the user in accordance to the doctor required rate"""

    try:
        consultation = Consultation.objects.get(id=consultation_id)
        dentist = Dentist.objects.get(id=consultation.dentist_id)
        balance = wallet.balance
        rate = dentist.consultation_rate

        if balance <= rate:
            return False
        else:
            time_capacity = balance / rate
            return timedelta(minutes=time_capacity)

    except:
        return None


def trigger_welcome_message(consultation_id):
    data = {
        "type": "welcome_message",
        "message": "Welcome to the Consultation Chat",
        "consultation_id": consultation_id
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('task', data)


def end_consultation_chat(consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)
        consultation.ending_time = timezone.now()
        data = {
            "type": "disconnect",
            "message": "This Consultation Chat has been terminated",
            "consultation_id": consultation_id
        }
        room_name = f'chat_{consultation_id}'

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(room_name, data)

    except:
        return None
