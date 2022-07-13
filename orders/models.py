from django.db import models
from django.contrib.auth import get_user_model
from campaign_statistics.models import Reward, Campaign

User = get_user_model()

TRANSACTION_STATUS_CHOICES = [
    ("PENDING", "PENDING"),
    ("TXN_SUCCESS", "TXN_SUCCESS"),
    ("TXN_FALIURE", "TXN_FALIURE"),
]


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    bonus = models.IntegerField(default=0)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)
    billing_address = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=11, choices=TRANSACTION_STATUS_CHOICES, default="Pending")
    rewards = models.ManyToManyField(Reward, blank=True)
    campaign = models.ForeignKey(Campaign, null=True, related_name='transactions', blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
