import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Message
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = text_data_json["sender_id"]
        sender = await sync_to_async(User.objects.get)(id=sender_id)

        #save message to database
        chat = await sync_to_async(Chat.objects.get)(id=self.chat_id)
        await self.save_message(chat, sender, message) #this line was wrong
    
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        #send message to Websocket
        await self.send(text_data=json.dumps({"message": message, "sender_id": sender_id}))

    @sync_to_async
    def save_message(self, chat, sender, text):
      Message.objects.create(chat=chat, sender=sender, text=text)
