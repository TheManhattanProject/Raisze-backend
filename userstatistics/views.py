from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from .models import FinancialSheets,SavedCampaigns
from .serializers import CreateFinancialSheetSerializer,CreateSavedCampaignsSerializer


class CreateFinancialSheetsView(generics.CreateAPIView):
    serializer_class = CreateFinancialSheetSerializer
    queryset=FinancialSheets.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data},context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateSaveCampaignsView(generics.CreateAPIView):
    serializer_class = CreateSavedCampaignsSerializer
    queryset=SavedCampaigns.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data},context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)