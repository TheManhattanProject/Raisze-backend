import json
from .models import Campaign
from .serializers import DetailCampaignSerializer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class CollectionStatus(AsyncWebsocketConsumer):
    async def connect(self):
        self.campaign_id = self.scope['url_route']['kwargs']['campaign_id']
        self.campaign = await database_sync_to_async(self.get_campaign)()
        self.room_group_name = self.campaign_id
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)

    def get_campaign(self):
        return Campaign.objects.get(campaign_id=self.campaign_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    async def funding_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'total_funding': message
        }))
