from users.models import Dentist, User
from .models import Consultation, ConsultationRequest
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(decoded_token):

    try:
        return User.objects.get(id=decoded_token['id'])
    except User.DoesNotExist:
        return None


@database_sync_to_async
def get_consultation(consultation_id):
    try:
        return Consultation.objects.get(id=consultation_id)
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
