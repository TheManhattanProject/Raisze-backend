from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Campaign, CampaignImage, Category, SubCategory
from rest_framework.views import APIView
from .serializers import *
from .pagination import *


class CreateTripView(generics.CreateAPIView):
    serializer_class = CreateCampaignSerializer
    queryset = Campaign.objects.all()

    def create(self, request, *args, **kwargs):
        # The request should be made in json format with POST
        serializer = self.get_serializer(
            data={**request.data, "creatorEmail": request.user.email})
        serializer.is_valid(raise_exception=True)
        campaign = self.perform_create(serializer)
        imagesList = []
        try:
            for image in request.data.get('images', []):
                imagesList.append(CampaignImage.objects.get(id=image))
        except Exception as e:
            print(e)
        campaign.campaign_images.add(*imagesList)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PopularCampaignsView(generics.ListAPIView):
    permission_classes = []

    def list(self, request, *args, **kwargs):
        cats = Category.objects.filter()
        queryset = Campaign.objects.all()
        response = {}
        for cat in cats:
            campaigns = queryset.filter(
                categorites__category=cat).distinct().order_by("-nor_score")
            if len(campaigns) > 20:
                campaigns = campaigns[:20]
            ser = ListCampaignSerializer(campaigns, many=True)
            response[cat.category_id] = ser.data
        return Response(response)


class CampaignListPagAPIView(generics.ListAPIView):
    serializer_class = ListCampaignSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Campaign.objects.all().order_by("-nor_score")
        category_name = self.request.GET.get('category', None)
        if category_name:
            queryset = queryset.filter(
                categorites__category__category_id=category_name).distinct().order_by("-nor_score")
        return queryset

class CampaignListUnPagAPIView(CampaignListPagAPIView):
    pagination_class = None


class SubPopularCampaignsView(generics.ListAPIView):
    permission_classes = []

    def list(self, request, *args, **kwargs):
        category_name = self.request.GET.get('category', None)
        category = Category.objects.get(category_id=category_name)
        cats = SubCategory.objects.filter(category=category)
        queryset = Campaign.objects.all()
        response = {}
        subresponse = {}
        for cat in cats:
            campaigns = queryset.filter(
                categorites__id=cat.id).distinct().order_by("-nor_score")
            if len(campaigns) > 20:
                campaigns = campaigns[:20]
            ser = ListCampaignSerializer(campaigns, many=True)
            subresponse[cat.category_id] = ser.data
        response['subcategories'] = subresponse
        campaigns = queryset.filter(
            categorites__category=category).distinct().order_by("-nor_score")
        if len(campaigns) > 20:
            campaigns = campaigns[:20]
        ser = ListCampaignSerializer(campaigns, many=True)
        response["category"] = ser.data
        return Response(response)


class UpdateCampaignAPIView(generics.UpdateAPIView):
    serializer_class = CreateCampaignSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Campaign.objects.filter(
                campaign_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Asset id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def update(self, request, *args, **kwargs):
        campaign = self.get_object()
        imagesList = []
        try:
            for image in request.data.get('images', []):
                imagesList.append(
                    CampaignImage.objects.get(id=image))
        except Exception as e:
            print(e)
        campaign.campaign_images.add(*imagesList)
        return super().update(request, *args, **kwargs)


class ListCreateCampaignImageAPIView(generics.ListCreateAPIView):
    serializer_class = ListCampaignImageSerializer
    queryset = CampaignImage.objects.filter()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
