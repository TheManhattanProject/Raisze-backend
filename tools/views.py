
from django.forms import ValidationError
from django.http import Http404
from rest_framework import generics,status
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from .models import ToolCategory, Valuation
from .models import Tools
from .serializers import *

# Create your views here.

class CreateValuationView(generics.CreateAPIView):
    serializer_class = CreateValuationSerializer
    query_set = Valuation.objects.all()
    permission_classes = []
    authentication_classes = []


class CreateToolsView(generics.CreateAPIView):
    queryset = Tools.objects.all()
    serializer_class = CreateToolsSerializer
    permission_classes = (IsAdminUser,)
    # authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tool = serializer.save()
        categoriesList = []
        try:
            for categorie in request.data.getlist('categories', []):
                categoriesList.append(
                    ToolCategory.objects.get(category_id=categorie))
        except Exception as e:
            print(e)
        tool.category.add(*categoriesList)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class UpdateToolsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateToolsSerializer
    permission_classes = (IsAdminUser,)
    # authentication_classes = []

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Tools.objects.filter(
                id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Tool id was not passed in the url")
        if activity.exists():
            activity[0].clicks += 1
            activity[0].save()
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListToolsView(generics.ListAPIView):
    queryset = Tools.objects.filter(is_deleted=False)
    serializer_class = CreateToolsSerializer
    permission_classes = []
    authentication_classes = []


class PopularToolsView(generics.ListAPIView):
    permission_classes = []

    def list(self, request, *args, **kwargs):
        cats = ToolCategory.objects.filter(is_deleted=False)
        queryset = Tools.objects.filter(is_deleted=False)
        response = {}
        for cat in cats:
            campaigns = queryset.filter(
                category=cat).distinct().order_by("-nor_score")
            if len(campaigns) > 20:
                campaigns = campaigns[:20]
            ser = CreateToolsSerializer(campaigns, many=True)
            response[cat.category_id] = ser.data
        return Response(response)


class ListCreateToolCategoryAPIView(generics.ListCreateAPIView):
    serializer_class = CreateToolCategorySerializer
    queryset = ToolCategory.objects.filter(is_deleted=False)


class ListCreateToolCategoryUnPagAPIView(ListCreateToolCategoryAPIView):
    pagination_class = None


class UpdateToolCategoryAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateToolCategorySerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = ToolCategory.objects.filter(
                campaign_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Tool Category id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
