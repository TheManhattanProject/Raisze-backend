from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Campaign, CampaignImage, Category, Gender, SubCategory, Tags
from rest_framework.views import APIView
from .serializers import *
from datetime import timedelta
from .pagination import *
from django.db import DatabaseError, transaction


class CreateTripView(generics.CreateAPIView):
    serializer_class = CreateCampaignSerializer
    queryset = Campaign.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

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


class ListCreateCampaignView(generics.ListCreateAPIView):
    serializer_class = CreateCampaignSerializer
    queryset = Campaign.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        # The request should be made in json format with POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign = self.perform_create(serializer)
        imagesList = []
        try:
            for image in request.data.get('images', []):
                imagesList.append(CampaignImage.objects.get(id=image))
        except Exception as e:
            print(e)
        campaign.campaign_images.add(*imagesList)
        gendersList = []
        try:
            for gender in request.data.get('genders', []):
                gendersList.append(Gender.objects.get(gender=gender))
        except Exception as e:
            print(e)
        campaign.campaign_gender.add(*gendersList)    
        tagsList = []
        try:
            for tag in request.data.get('tags', []):
                tagsList.append(Tags.objects.get(tags=tag))
        except Exception as e:
            print(e)
        campaign.campaign_tags.add(*tagsList)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class PopularCampaignsView(generics.ListAPIView):
    permission_classes = []

    def list(self, request, *args, **kwargs):
        cats = Category.objects.filter()
        queryset = Campaign.objects.filter(is_deleted=False)
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
        queryset = Campaign.objects.filter(is_deleted=False).order_by("-nor_score")
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
        queryset = Campaign.objects.filter(is_deleted=False)
        response = {}
        subresponse = {}
        for cat in cats:
            campaigns = queryset.filter(
                categorites__id=cat.id).distinct().order_by("-nor_score")
            if len(campaigns) > 8:
                campaigns = campaigns[:8]
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


class UpdateCampaignAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailCampaignSerializer

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
    
    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateCampaignImageAPIView(generics.ListCreateAPIView):
    serializer_class = ListCampaignImageSerializer
    queryset = CampaignImage.objects.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ListCreateCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCategorySerializer
    queryset = Category.objects.filter(is_deleted=False)


class ListCreateCategoryUnPagAPIView(ListCreateCategoryAPIView):
    pagination_class = None

class UpdateCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateCategorySerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Category.objects.filter(
                campaign_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Category id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListCreateSubCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = CreateSubCategorySerializer
    queryset = SubCategory.objects.filter(is_deleted=False)

class ListCreateSubCategoryUnPagAPIView(ListCreateSubCategoryAPIView):
    pagination_class = None

class UpdateSubCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateSubCategorySerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = SubCategory.objects.filter(id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("SubCategory id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCategorySerializer
    queryset = Category.objects.filter(is_deleted=False)


class ListCreateCategoryUnPagAPIView(ListCreateCategoryAPIView):
    pagination_class = None


class UpdateCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateCategorySerializer

    def get_object(self):
        if self.kwargs.get('category_id'):
            activity = Category.objects.filter(
                campaign_id=self.kwargs.get('category_id'), is_deleted=False)
        else:
            raise ValidationError("Category id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateItemsAPIView(generics.ListCreateAPIView):
    serializer_class = CreateItemsSerializer
    queryset = Items.objects.filter(is_deleted=False)


class ListCreateItemsUnPagAPIView(ListCreateItemsAPIView):
    pagination_class = None


class UpdateItemsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateItemsSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Items.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Items id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateRewardAPIView(generics.ListCreateAPIView):
    serializer_class = CreateRewardSerializer
    queryset = Reward.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        # The request should be made in json format with POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reward = self.perform_create(serializer)
        itemsList = []
        try:
            for item_id in request.data.get('items', []):
                itemsList.append(Items.objects.get(id=item_id))
        except Exception as e:
            print(e)
        reward.items.clear()
        reward.items.add(*itemsList)
        reward.aassociated_campaign = Campaign.objects.get(campaign_id=request.data.get('campaign_id', None))
        reward.reward_estimated_delivery_time = timedelta(
            days=int(request.data.get('estimated_delivery_time', 10)))
        reward.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateRewardAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateRewardSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Reward.objects.filter(
                reward_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Reward id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def update(self, request, *args, **kwargs):
        reward = self.get_object()
        if request.data.get("clear_items", False):
            reward.items.clear()
        if request.data.get('items', []):
            itemsList = []
            try:
                for item_id in request.data.get('items', []):
                    itemsList.append(Items.objects.get(id=item_id))
            except Exception as e:
                print(e)
            reward.items.add(*itemsList)
        if request.data.get('campaign_id', None):
            reward.aassociated_campaign = Campaign.objects.get(
                campaign_id=request.data.get('campaign_id', None))
        if request.data.get('estimated_delivery_time'):
            reward.reward_estimated_delivery_time = timedelta(
                days=int(request.data.get('estimated_delivery_time', 10)))
        reward.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
