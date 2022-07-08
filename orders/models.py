from django.db import models
from django.contrib.auth import get_user_model
from campaign_statistics.models import Reward, Campaign

User = get_user_model()

TRANSACTION_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
]


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default="Pending")
    rewards = models.ManyToManyField(Reward, blank=True)
    campaign = models.ForeignKey(Campaign, null=True, related_name='transactions', blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
