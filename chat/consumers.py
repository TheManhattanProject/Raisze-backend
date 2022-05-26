import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from Crypto.Cipher import Blowfish
from struct import pack
from asgiref.sync import sync_to_async
from chat.models import *
from raisze_backend.settings import SECRET_KEY


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        cipher = Blowfish.new(bytes(SECRET_KEY, encoding="acsii"), Blowfish.MODE_CBC)
        # self.chat_id = cipher.decrypt(self.scope['url_route']['kwargs']['room_name'])
        self.user = self.scope['user']
        self.room_group_name = self.room_name
        self.chatroom = await database_sync_to_async(self.get_chatroom)()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        if(await database_sync_to_async(self.check_user)()):
            await self.accept()
            await self.earlier_messages(self.chatroom)

    def check_user(self):
        if self.user in self.chatroom.users.all():
            return True
        return False

    def get_chatroom(self):
        users_id = self.room_name.split("_")
        users_id.sort()
        self.chat_id = "_".join(users_id)
        chatroom, created = ChatRoom.objects.get_or_create(name=self.chat_id)
        if created:
            chatroom.users.add(*CustomUser.objects.filter(id__in=users_id))
            chatroom.save()
        return chatroom

    def get_messages(self, chatroom):
        return chatroom.messages.filter()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await database_sync_to_async(self.save_message)(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def get_text(self, messages):
        lis = []
        for message in messages:
            lis.append(message.text)
        return lis

    async def earlier_messages(self, chatroom):
        message = await database_sync_to_async(self.get_messages)(chatroom)
        data = await sync_to_async(self.get_text)(message)
        await self.send(text_data=json.dumps({
            'message': data
        }))

    def save_message(self, text):
        Message.objects.create(text=text, chatroom=self.chatroom)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
