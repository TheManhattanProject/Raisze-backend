from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Campaign, CampaignImage, Reward



class CreateCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'

    # def create(self, validated_data):
    #     creator=get_user_model().objects.get(email=validated_data["creatorEmail"])
    #     validated_data.pop("creatorEmail")
    #     trip=Trips(creator=creator,**validated_data)
    #     trip.save()
    #     TripRating.objects.create(trip=trip)
    #     return trip

class CreateRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'


class CreateRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'

class ListCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        exclude = ("categorites",)
        read_only_fields = ('campaign_images',)


class ListCampaignImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignImage
        fields = ('image','id')
