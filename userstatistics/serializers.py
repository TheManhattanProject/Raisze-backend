from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FinancialSheets,SavedCampaigns
from campaign_statistics.models import Campaign



class CreateFinancialSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSheets
        fields = ('sheets',)

    def create(self, validated_data):
        print(validated_data)
        obj=FinancialSheets(sheet_owner=self.context.get('user'),**validated_data)
        obj.save()
        return obj


class CreateSavedCampaignsSerializer(serializers.ModelSerializer):
    campaign_id=serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = SavedCampaigns
        fields = ('campaign_id',)

    def create(self, validated_data):
        print(validated_data)
        print(validated_data["campaign_id"])
        obj,_=SavedCampaigns.objects.get_or_create(profile=self.context.get('user'),)
        obj.campaigns.add(Campaign.objects.get(campaign_id=validated_data["campaign_id"]))
        obj.save()
        return obj
