import json
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from users.models import User
from .models import Appointment, AppointmentMessage
from rest_framework.permissions import AllowAny

from appointment.utils import get_appointment


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        chat_id = self.scope['url_route']['kwargs']['appointment_id']
        appointment = get_appointment(chat_id)

        self.room_name = f"appointment_thread_{appointment_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
