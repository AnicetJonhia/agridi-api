import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Group

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'chat_{self.group_id}'

        # Joindre le groupe de chat
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        group = await Group.objects.get(id=self.group_id)
        msg = Message.objects.create(content=message, sender_id=sender_id, group=group)

        # Envoyer le message à tous les membres du groupe
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'sender_id': sender_id,
                'timestamp': str(msg.timestamp)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        timestamp = event['timestamp']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'timestamp': timestamp
        }))
