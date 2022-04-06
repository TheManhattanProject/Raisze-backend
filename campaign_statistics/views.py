from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from .models import Campaign
from .serializers import CreateCampaignSerializer


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