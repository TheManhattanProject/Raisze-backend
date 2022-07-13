from rest_framework import serializers
from .models import *
from users.serializers import UserViewSerializer
from campaign_statistics.serializers import ListCampaignSerializer, CreateRewardSerializer


class CreateTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'order_id', 'made_by', 'checksum')


class ListTransactionSerializer(serializers.ModelSerializer):
    made_by = UserViewSerializer()
    campaign = ListCampaignSerializer()
    rewards = CreateRewardSerializer(many=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'order_id', 'made_by', 'checksum')

