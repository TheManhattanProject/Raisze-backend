from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from .models import Campaign, Category
from rest_framework.views import APIView
from .serializers import *
from .pagination import *

class CreateTripView(generics.CreateAPIView):
    serializer_class = CreateCampaignSerializer
    queryset=Campaign.objects.all()

    def create(self, request, *args, **kwargs):
        # The request should be made in json format with POST
        serializer = self.get_serializer(data={**request.data,"creatorEmail":request.user.email})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PopularCampaignsView(generics.ListAPIView):
    permission_classes = []
    
    def list(self, request, *args, **kwargs):
        cats = Category.objects.filter()
        queryset = Campaign.objects.all()
        response = {}
        for cat in cats:
            campaigns = queryset.filter(categorites__category=cat).distinct().order_by("-nor_score")
            if len(campaigns) > 20:
                campaigns = campaigns[:20]
            ser = ListCampaignSerializer(campaigns, many=True)
            response[cat.category_id] = ser.data
        return Response(response)
        

class CampaignListAPIView(generics.ListAPIView):
    serializer_class = ListCampaignSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = []

    def get_queryset(self):
        queryset = Campaign.objects.all()
        category_name = self.request.GET.get('category', None)
        if category_name:
            queryset = queryset.filter(
                categorites__category__category_id=category_name).distinct().order_by("-nor_score")
        return queryset
