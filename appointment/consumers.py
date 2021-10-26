import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        appointment_id = self.scope['url_route']['kwargs']['appointment_id']
        self.room_name = f"appointment_thread_{appointment_id}"
        sync_to_async(self.channel_layer.group_add)(self.room_name, self.channel_name)

        self.send({
            "type": "websocket.accept"
        })        
        
        return super().websocket_connect(message)
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
