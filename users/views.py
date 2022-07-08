from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import UpdateUserSerializer
# Create your views here.



class UpdateUser(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = get_user_model().objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        if self.kwargs.get('id'):
            activity = get_user_model().objects.filter(id=self.kwargs.get('id'))
        else:
            raise ValidationError("User id was not passed in the url")
        if activity.exists():
            return activity[0]
        else:
            raise Http404
