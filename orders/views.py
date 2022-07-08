from django.forms import ValidationError
from django.conf import settings
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from .serializers import *
from campaign_statistics.models import Reward
from rest_framework.views import APIView
from rest_framework import generics
from utils.paytm import generate_checksum


class PaymentAPIView(generics.CreateAPIView):
    serializer_class = CreateTransactionSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        rewards_id = request.data.getlist('reward', [])
        rewards = Reward.objects.filter(reward_id__in=rewards_id)
        amount = int(request.data.get('amount', 0)) + int(request.data.get('bonus', 0))
        campaign = Campaign.objects.get(campaign_id=request.data['campaign_id'])
        transaction = Transaction.objects.create(made_by=user, amount=amount, campaign=campaign)
        transaction.rewards.add(*rewards)
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        )
        paytm_params = dict(params)
        if transaction.order_id is None:
            transaction.order_id = transaction.made_on.strftime(
                'PAY2ME%Y%m%dODR') + str(transaction.id)
        transaction.save()
        checksum = generate_checksum(paytm_params, merchant_key)
        transaction.checksum = checksum
        transaction.save()
        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        serializer = CreateTransactionSerializer(transaction)
        return Response({**serializer.data, **paytm_params}, status=status.HTTP_201_CREATED)


class UpdateTransactionAPIView(generics.UpdateAPIView):
    serializer_class = CreateTransactionSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Transaction.objects.filter(
                id=self.kwargs.get('id')).exclude(status="Rejected")
        else:
            raise ValidationError("Transaction id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404
