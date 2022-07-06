from django.utils import timezone
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Campaign, CampaignImage, Category, Country, Gender, SubCategory, Tags
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


class ListCreateCampaignAPIView(generics.ListCreateAPIView):
    serializer_class = CreateCampaignSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            self.serializer_class = ListCampaignSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = Campaign.objects.filter(
            is_deleted=False).order_by("-nor_score")
        category_name = self.request.GET.get('category', None)
        if category_name:
            queryset = queryset.filter(
                categorites__category__category_id=category_name).distinct().order_by("-nor_score")
        return queryset


    def create(self, request, *args, **kwargs):
        if request.data.get('duration'):
            duration = request.data.get('duration')
            try:
                duration = int(duration)
                request.data['campaign_duration'] = timezone.now() + timedelta(days=duration)
            except ValueError:
                request.data['campaign_duration'] = duration
        # The request should be made in json format with POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        campaign = serializer.save()
        imagesList = []
        try:
            for image in request.data.getlist('images', []):
                imagesList.append(CampaignImage.objects.get(id=image))
        except Exception as e:
            print(e)
        campaign.campaign_images.add(*imagesList)
        subcategoriesList = []
        try:
            for subcategorie in request.data.getlist('subcategories', []):
                subcategoriesList.append(SubCategory.objects.get(subcategory_id=subcategorie))
        except Exception as e:
            print(e)
        campaign.categorites.add(*subcategoriesList)
        gendersList = []
        try:
            for gender in request.data.getlist('genders', []):
                gendersList.append(Gender.objects.get(gender=gender))
        except Exception as e:
            print(e)
        campaign.campaign_gender.add(*gendersList)    
        tagsList = []
        try:
            for tag in request.data.getlist('tags', []):
                tagsList.append(Tags.objects.get(tags=tag))
        except Exception as e:
            print(e)
        campaign.campaign_tags.add(*tagsList)
        timelinesList = []
        try:
            for timeline in request.data.getlist('timelines', []):
                timelinesList.append(Timeline.objects.get(id=timeline))
        except Exception as e:
            print(e)
        campaign.timelines.add(*timelinesList)
        headers = self.get_success_headers(serializer.data)
        # if request.data.get('country'):
            # campaign.country_of_origin = Country.objects.get(country_name=request.data.get('country'))
        # if request.data.get('duration'):
        #     duration = request.data.get('duration')
        #     try:
        #         duration = int(duration)
        #         campaign.campaign_duration = timezone.now() + timedelta(days=duration)
        #     except ValueError:
        #         campaign.campaign_duration = duration
        # campaign.save()
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
            raise ValidationError("Campaign id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def update(self, request, *args, **kwargs):
        campaign = self.get_object()
        imagesList = []
        try:
            for image in request.data.getlist('images', []):
                imagesList.append(CampaignImage.objects.get(id=image))
        except Exception as e:
            print(e)
        if imagesList:
            campaign.campaign_images.clear()
            campaign.campaign_images.add(*imagesList)
        subcategoriesList = []
        try:
            for subcategorie in request.data.getlist('subcategories', []):
                subcategoriesList.append(SubCategory.objects.get(subcategory_id=subcategorie))
        except Exception as e:
            print(e)
        if subcategoriesList:
            campaign.categorites.clear()
            campaign.categorites.add(*subcategoriesList)
        gendersList = []
        try:
            for gender in request.data.getlist('genders', []):
                gendersList.append(Gender.objects.get(gender=gender))
        except Exception as e:
            print(e)
        if gendersList:
            campaign.campaign_gender.clear()    
            campaign.campaign_gender.add(*gendersList)    
        tagsList = []
        try:
            for tag in request.data.getlist('tags', []):
                tagsList.append(Tags.objects.get(tags=tag))
        except Exception as e:
            print(e)
        if tagsList:
            campaign.campaign_tags.clear()
            campaign.campaign_tags.add(*tagsList)
        timelinesList = []
        try:
            for timeline in request.data.getlist('timelines', []):
                timelinesList.append(Timeline.objects.get(id=timeline))
        except Exception as e:
            print(e)
        if timelinesList:
            campaign.timelines.clear()
            campaign.timelines.add(*timelinesList)
        # if request.data.get('country'):
            # campaign.country_of_origin = Country.objects.get(country_name=request.data.get('country'))
        if request.data.get('duration'):
            duration = request.data.get('duration')
            try:
                duration = int(duration)
                campaign.campaign_duration = timezone.now() + timedelta(days=duration)
            except ValueError:
                campaign.campaign_duration = duration
            campaign.save()
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


class CreateCommentForCampaignAPIView(generics.CreateAPIView):
    serializer_class = ListCreateCommentSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Campaign.objects.filter(
                campaign_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Campaign id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    
    def create(self, request, *args, **kwargs):
        campaign = self.get_object()
        Comment.objects.create(created_by=request.user, campaign=campaign, message=request.data.get('message'))
        return Response(status=status.HTTP_201_CREATED)


class CreateReplyForCampaignAPIView(generics.CreateAPIView):
    serializer_class = ListCreateReplySerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Comment.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Comment id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    
    def create(self, request, *args, **kwargs):
        comment = self.get_object()
        Reply.objects.create(created_by=request.user, comment=comment, message=request.data.get('message'))
        return Response(status=status.HTTP_201_CREATED)

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
    
    def get_queryset(self):
        queryset = SubCategory.objects.filter(is_deleted=False)
        if self.request.GET.get('category'):
            queryset = queryset.filter(category=Category.objects.get(
                category_id=self.request.GET.get('category')))
        return queryset

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


class ListCreateTimelineAPIView(generics.ListCreateAPIView):
    serializer_class = CreateTimelineSerializer
    queryset = Timeline.objects.filter(is_deleted=False)


class ListCreateTimelineUnPagAPIView(ListCreateTimelineAPIView):
    pagination_class = None


class UpdateTimelineAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateTimelineSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Timeline.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Timeline id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateTagsAPIView(generics.ListCreateAPIView):
    serializer_class = CreateTagsSerializer
    queryset = Tags.objects.filter(is_deleted=False)


class ListCreateTagsUnPagAPIView(ListCreateTagsAPIView):
    pagination_class = None


class UpdateTagsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateTagsSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Tags.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Tags id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCreateGenderAPIView(generics.ListCreateAPIView):
    serializer_class = CreateGenderSerializer
    queryset = Gender.objects.filter(is_deleted=False)


class ListCreatGenderUnPagAPIView(ListCreateGenderAPIView):
    pagination_class = None


class UpdateGenderAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateGenderSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Gender.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Gender id was not passed in the url")
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
