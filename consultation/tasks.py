from celery import shared_task
from consultation.utils import end_consultation_chat


@shared_task
def terminate_consultation_chat(consultation_chat_id):
    end_consultation_chat(consultation_chat_id)
