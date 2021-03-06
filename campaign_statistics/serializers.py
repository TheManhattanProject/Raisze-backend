from email.message import Message
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Campaign, CampaignImage, Category, Comment, Gender, Items, Recommendations, Reply, Reward, Shipping, SubCategory, Tags, Timeline
from users.serializers import UserSerializer
from django.core.paginator import Paginator
from orders.models import Transaction
from users.serializers import UserViewSerializer


class TransactionViewSerializer(serializers.ModelSerializer):
    made_by = UserViewSerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'made_by', 'bonus', 'shipping_address', 'billing_address', 'rewards')

class ListShippingSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields = ('country',)

    def get_country(self, instance):
        if instance.country:
            return instance.country.country_name
        return None

class ListCreateReplySerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Reply
        fields = ('id', 'created_at', 'message', 'created_by')
        read_only_fields = ('created_by',)


class ListCreateCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    created_by = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'message', 'created_by', 'replies')
        read_only_fields = ('created_by',)

    def get_replies(self, instance):
        replies = instance.replies.filter(is_deleted=False)
        return ListCreateReplySerializer(replies, many=True).data


class CreateCampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('images', 'categorites', 'nor_score', 
                            'campaign_gender', 'campaign_tags', 'timelines')

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
                  'campaign_id')


class CampaignViewSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ('title', 'subtitle', 'cover_image', 'video_link',
                  'campaign_launch_date', 'campaign_verification_success',
                  'campaign_detail_completed', 'campaign_launch_date', 'campaign_duration',
                  'campaign_total_funded', 'campaign_goal_amount', 'country_of_origin',
                  'campaign_id', 'transactions')

    def get_transactions(self, instance):
        transactions = Transaction.objects.filter(status="TXN_SUCCESS", campaign=instance)
        return TransactionViewSerializer(transactions, many=True).data


class DetailCampaignSerializer(serializers.ModelSerializer):
    recommendations = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('images', 'categorites', 'campaign_admin', 'country_of_origin', 'nor_score',
                            'campaign_gender', 'campaign_tags', 'timelines', 'campaign_duration', 'reccomendations', 'comments', 'transactions')
        depth = 1

    def get_recommendations(self, instance):
        recommendation = Recommendations.objects.get(main_model=instance)
        return ListCampaignSerializer(recommendation.recommended_models.filter(is_deleted=False), many=True).data

    def get_comments(self, instance):
        comments = instance.comments.filter(is_deleted=False)
        return ListCreateCommentSerializer(comments, many=True).data

    def get_transactions(self, instance):
        page = self.context.get('request').GET.get('transaction_page', 1)
        queryset = Transaction.objects.filter(campaign=instance, status="TXN_SUCCESS")
        paginator = Paginator(queryset, 20)
        page = paginator.page(page)
        return {"data":TransactionViewSerializer(page.object_list, many=True).data, "has_next":page.has_next()}


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
        read_only_field = ("category",)


class CreateRewardSerializer(serializers.ModelSerializer):
    # shippings = ListShippingSerializer(many=True)

    class Meta:
        model = Reward
        fields = '__all__'
        read_only_field = (
            "is_deleted", "items", "associated_campaign", "reward_estimated_delivery_time", "shippings")


# class ListCampaignSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Campaign
#         exclude = ("categorites",)
#         read_only_fields = ('campaign_images',)


class ListCampaignImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampaignImage
        fields = ('image', 'id')

