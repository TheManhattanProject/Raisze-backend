from amqp import RecoverableChannelError
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

REWARD_TYPE_CHOICES = [
    ("Digital", "Digital"),
    ("Physical", "Physical"),
    ("Both", "Both")
]



class Category(models.Model):
    category_id=models.CharField(max_length=256, unique=True)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.category_id

class SubCategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True, null=True,)
    subcategory_id=models.CharField(max_length=256, unique=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.subcategory_id


class Country(models.Model):
    country_name=models.CharField(max_length=256, unique=True)
    def __str__(self):
        return self.country_name



def campaign_cover_image_directory_path(instance, filename):
    return 'campaign_cover_image_{0}/{1}'.format(instance.campaign_id, filename)


class CampaignImage(models.Model):
    image = models.ImageField()
    is_deleted = models.BooleanField(default=False)


class Gender(models.Model):
    gender=models.CharField(max_length=256, unique=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.gender


class Tags(models.Model):
    tags=models.CharField(max_length=256)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.tags


class Timeline(models.Model):
    target_time = models.DateTimeField()
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

class Campaign(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    categorites=models.ManyToManyField(SubCategory,blank=True)
    campaign_id=models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    campaign_admin=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,blank=True, null=True,)
    country_of_origin=models.ForeignKey(Country,on_delete=models.SET_NULL,blank=False, null=True,)
    title=models.CharField(max_length=256)
    subtitle=models.TextField()
    cover_image=models.ImageField(upload_to=campaign_cover_image_directory_path)
    video_link=models.TextField()
    campaign_detail_completed=models.BooleanField(default=False)
    campaign_verification_success=models.BooleanField(default=False)
    campaign_launch_date=models.DateTimeField(blank=True,null=True)
    campaign_duration=models.DateTimeField(blank=True,null=True)
    campaign_total_funded=models.DecimalField(max_digits=14,decimal_places=2)
    campaign_goal_amount=models.DecimalField(max_digits=12,decimal_places=2)
    campaign_currency=models.CharField(max_length=256)
    campaign_project_description=models.TextField()
    campaign_risk_challenges=models.TextField()
    campaign_environment_commitment=models.TextField()
    campaign_bank_account_no=models.CharField(max_length=256)
    campaign_bank_account_ifsc=models.CharField(max_length=256)
    campaign_age_range_min=models.IntegerField()
    campaign_age_range_max=models.IntegerField()
    nor_score = models.DecimalField(default=0, decimal_places=4, max_digits=5)
    campaign_gender=models.ManyToManyField(Gender,blank=True)
    campaign_tags=models.ManyToManyField(Tags,blank=True)
    campaign_images = models.ManyToManyField(CampaignImage, blank=True)
    timelines = models.ManyToManyField(Timeline, blank=True)
    funding_distribution = models.JSONField()
    is_deleted = models.BooleanField(default=False)
    score_ignore = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.campaign_total_funded >= self.campaign_goal_amount:
            self.is_deleted = True
        super(Campaign, self).save(*args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(self.campaign_id), {
                'type': 'funding_message',
                'message': float(self.campaign_total_funded)
            })


class Recommendations(models.Model):
    main_model = models.OneToOneField(Campaign, related_name="recommendations", on_delete=models.CASCADE)
    recommended_models = models.ManyToManyField(Campaign, blank=True, related_name="recommended_to")


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="comments")
    is_deleted = models.BooleanField(default=False)


class Reply(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="replies")
    message = models.TextField()
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies")
    is_deleted = models.BooleanField(default=False)


class Items(models.Model):
    item_title=models.CharField(max_length=256)
    item_quantity=models.BigIntegerField()
    is_deleted=models.BooleanField(default=False)

def reward_image_directory_path(instance, filename):
    return 'reward_image_{0}/{1}'.format(instance.reward_id, filename)

class Shipping(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_everywhere = models.BooleanField(default=False)



class Reward(models.Model):
    class Shippingk(models.TextChoices):
        ONE = '1', "Shipped through email"
        TWO = '2', "Shipping restricted to certain countries"
        THREE = '3', "Anywhere in the world"


    shippings = models.ManyToManyField(Shipping, blank=True)
    reward_id=models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    reward_image=models.ImageField(upload_to=reward_image_directory_path)
    associated_campaign=models.ForeignKey(Campaign,on_delete=models.SET_NULL,blank=True, null=True,)
    reward_title=models.CharField(max_length=256)
    reward_description=models.TextField()
    reward_amount=models.DecimalField(max_digits=12,decimal_places=2)
    items=models.ManyToManyField(Items,blank=True)
    reward_type = models.TextField(max_length=10, choices=REWARD_TYPE_CHOICES)
    reward_shipping=models.CharField(max_length=256,choices=Shippingk.choices,default=Shippingk.THREE)
    reward_estimated_delivery_time=models.DurationField(null=True, blank=True)
    reward_quantity_is_unlimited=models.BooleanField(default=False)
    reward_quantity=models.BigIntegerField()
    reward_quantity_left=models.BigIntegerField()    
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.reward_title