# chat/channels.py
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id
        print(f'User connected to chat {self.chat_id}, group: {self.room_group_name}')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        chat_type = text_data_json['type']

        print(f'Received message: {message}, sender_id: {sender_id}, type: {chat_type}')
        User = get_user_model()
        user = await sync_to_async(User.objects.get)(id=sender_id)
        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)

        await sync_to_async(Message.objects.create)(chat=chat, sender=user, text=message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        print(f'Sending message: {message}, sender_id: {sender_id}, type: chat_message') 

        await self.send(text_data=json.dumps({
            'type':'chat_message', 
            'message': message,
            'sender_id': sender_id,
        }))
