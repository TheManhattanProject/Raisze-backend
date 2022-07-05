import json
from .models import Campaign
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import time


class CollectionStatus(AsyncWebsocketConsumer):
    async def connect(self):
        self.accept()
        self.campaign_id = self.scope['url_route']['kwargs']['campaign_id']
        self.campaign = await database_sync_to_async(self.get_campaign)()
        print("yesnfijani")


    async def disconnect(self, close_code=None):
        pass

    def get_campaign(self):
        time.sleep(10)
        return Campaign.objects.get(campaign_id=self.campaign_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
