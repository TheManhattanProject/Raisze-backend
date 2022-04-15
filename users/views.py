from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import UpdateUserSerializer
# Create your views here.



class UpdateUser(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = get_user_model().objects.all()
    
    def update(self, request, *args, **kwargs):
        serializer = UpdateUserSerializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)