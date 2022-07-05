from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Campaign, CampaignImage, Category, Gender, Items, Reward, SubCategory, Tags, Timeline



class CreateCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('images', 'categorites', 'campaign_admin',  'nor_score', 'campaign_gender', 'campaign_tags', 'timelines')

    # def create(self, validated_data):
    #     creator=get_user_model().objects.get(email=validated_data["creatorEmail"])
    #     validated_data.pop("creatorEmail")
    #     trip=Trips(creator=creator,**validated_data)
    #     trip.save()
    #     TripRating.objects.create(trip=trip)
    #     return trip

class ListCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ('title', 'subtitle', 'cover_image', 'video_link',
                  'campaign_launch_date', 'campaign_verification_success',
                  'campaign_detail_completed', 'campaign_launch_date', 'campaign_duration',
                  'campaign_total_funded', 'campaign_goal_amount', 'country_of_origin',
                  'campaign_id',)


class DetailCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('images', 'categorites', 'campaign_admin', 'country_of_origin', 'nor_score', 'campaign_gender', 'campaign_tags', 'timelines', 'campaign_duration')
        depth = 1

class CreateRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'


class CreateCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CreateTimelineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timeline
        fields = '__all__'


class CreateGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class CreateTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'

class CreateItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'


class CreateSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'
        read_only_field=("category",)


class CreateRewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'
        read_only_field = (
            "is_deleted", "items", "associated_campaign", "reward_estimated_delivery_time")


# class ListCampaignSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Campaign
#         exclude = ("categorites",)
#         read_only_fields = ('campaign_images',)


class ListCampaignImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignImage
        fields = ('image','id')
