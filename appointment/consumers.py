import json
from channels.generic.websocket import WebsocketConsumer




class ChatConsumer(WebsocketConsumer):

    def connect(self):
        appointment_id = self.scope['url_route']['kwargs']['appointment_id']
        self.room_name = f"appointment_thread_{appointment_id}"

        
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
