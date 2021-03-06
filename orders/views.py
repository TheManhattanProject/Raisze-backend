from locale import currency
from django.shortcuts import render
from django.views import View
from django.forms import ValidationError
from django.conf import settings
from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from .serializers import *
from campaign_statistics.models import Reward
from rest_framework.views import APIView
import requests
import json
import paytmchecksum
from django.db.models import Sum
from rest_framework import generics
from utils.paytm import generate_checksum
from campaign_statistics.models import Country
from campaign_statistics.serializers import CreateRewardSerializer


class PaymentAPIView(generics.CreateAPIView):
    serializer_class = CreateTransactionSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        country = Country.objects.get(country_name=request.data.get('country'))
        rewards_id = request.data.getlist('rewards', [])
        print(rewards_id)
        rewards = Reward.objects.filter(reward_id__in=rewards_id)
        amount = int(request.data.get('amount', 0)) 
        for reward in rewards:
            if reward.reward_type == "Digital":
                continue
            ship = reward.shippings.filter(country=country).first()
            print(rewards, ship, country, reward.shippings.all())
            if ship:
                amount += ship.cost
            else:
                ship = reward.shippings.filter(is_everywhere=True).first()
                if ship:
                    amount += ship.cost
                else:
                    return Response({**CreateRewardSerializer(reward).data, "status":"This reward is not available in your country"})
        if rewards:
            amount += rewards.aggregate(Sum('reward_amount')).get('reward_amount__sum')
        campaign = Campaign.objects.get(campaign_id=request.data['campaign_id'], status="Pending")
        transaction = Transaction.objects.create(made_by=user, amount=amount, campaign = campaign,
                                                 bonus=int(request.data.get('bonus', 0)), shipping_address=request.data.get('shipping_address', None),
                                                 billing_address=request.data.get('billing_address', None))
        amount += int(request.data.get('bonus', 0))
        transaction.rewards.add(*rewards)
        merchant_key = settings.PAYTM_SECRET_KEY
        transaction.order_id = transaction.made_on.strftime('PAY2ME%Y%m%dODR') + str(transaction.id)
        paytmParams = dict()
        paytmParams["body"] = {
            "requestType": "Payment",
            "mid": settings.PAYTM_MERCHANT_ID,
            "websiteName": settings.PAYTM_WEBSITE,
            "orderId": transaction.order_id,
            "txnAmount": {
                "value": str(amount),
                "currency": campaign.campaign_currency,
            },
            "callbackUrl": "https://backend.raisze.space/api/callback/",
            "userInfo": {
                "custId": "CUST_"+str(user.id),
                "mobile":9811370404
            },
        }
        transaction.save()
        checksum = paytmchecksum.generateSignature(
            json.dumps(paytmParams["body"]), merchant_key)
        transaction.checksum = checksum
        transaction.save()
        paytmParams["head"] = {
            "signature": checksum
        }
        post_data = json.dumps(paytmParams)

        # for Staging
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid="+settings.PAYTM_MERCHANT_ID+"&orderId="+transaction.order_id
        print(transaction.order_id)
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        if "txnToken" in response["body"]:
            token = response["body"]["txnToken"]
        else:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        transaction.token = token
        transaction.save()
        serializer = CreateTransactionSerializer(transaction).data
        return Response({"txnToken": token, **serializer}, status=status.HTTP_201_CREATED)


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

    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        paytmParams = dict()

        paytmParams["body"] = {
            "mid" : settings.PAYTM_MERCHANT_ID,
            "orderId" : transaction.order_id,
        } 
        checksum = paytmchecksum.generateSignature(
            json.dumps(paytmParams["body"]), settings.PAYTM_SECRET_KEY)
        paytmParams["head"] = {
            "signature"	: checksum
        }
        post_data = json.dumps(paytmParams)
        url = "https://securegw-stage.paytm.in/v3/order/status"

        response = requests.post(url, data=post_data,  headers={
                         "Content-type": "application/json"}).json()
        status_real = response['body']['resultInfo']['resultStatus']
        print(status_real)
        print(request.data.get('status', 'not'))
        if status_real == "TXN_FAILURE" and request.data.get('status','not') == "Approved":
            return Response("Transaction not done", status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class CallbackAPIView(generics.ListAPIView):
    serializer_class = CreateTransactionSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print(request.data)
        print("yes")
        order_id = request.data.get('ORDERID')
        body = {'mid':settings.PAYTM_MERCHANT_ID,'orderId':order_id}
        checksum = request.data.get('CHECKSUMHASH')
        transaction = Transaction.objects.filter(order_id=order_id).first()
        paytmParams = dict()
        paytmParams = dict(request.data)
        paytmChecksum = paytmParams['CHECKSUMHASH'][0]
        for key in paytmParams:
            paytmParams[key] = paytmParams[key][0]
        isVerifySignature = paytmchecksum.verifySignature(
        paytmParams, settings.PAYTM_SECRET_KEY, paytmChecksum)
        print(isVerifySignature, checksum)
        if isVerifySignature:
            transaction.status = request.data.get('STATUS')
        transaction.save()
        return Response(CreateTransactionSerializer(transaction).data)



class PaymentView(View):

    def get(self, request, id):
        transaction = Transaction.objects.get(id=id)
        token = transaction.token
        return render(request, 'payments.html', {'token':token, 'mid':settings.PAYTM_MERCHANT_ID, 'order_id':transaction.order_id})


class UserTransactionListAPIView(generics.ListAPIView):
    serializer_class = ListTransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(made_by=self.request.user)
        return queryset