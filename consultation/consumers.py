import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from users.models import User
from .models import ConsultationMessage, Consultation
from .utils import get_consultation, verify_consultation_user


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Receive the consultation id through the kwargs
        chat_id = self.scope['url_route']['kwargs']['consultation_id']
        consultation = get_consultation(chat_id)
        print(chat_id)

        user = self.scope.get('user', False)

        if not user:
            await self.accept()
            self.send(text_data=json.dumps({
                'type': 'message',
                'date': {
                    'messge': "Unauthorized Access"
                }
            }))
            await self.close()
        elif not consultation:
            await self.accept()
            self.send(text_data=json.dumps({
                'type': 'message',
                'date': {
                    'messge': "Invalid Consultation Data"
                }
            }))
            await self.close()
        elif not verify_consultation_user(consultation, user):
            await self.accept()
            self.send(text_data=json.dumps({
                'type': 'message',
                'date': {
                    'messge': "Unauthorized Access"
                }
            }))
            await self.close()

        self.user = user

        # Add Chat name from the consultation uuid id
        self.room_name = f'chat_{chat_id}'
        # print(self.room_name)
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
