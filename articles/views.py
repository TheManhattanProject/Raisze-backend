from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Article
from .serializers import CreateArticleSerializer, ListArticleSerializer

# Create your views here.
class CreatePostView(generics.CreateAPIView):

    serializer_class = CreateArticleSerializer
    queryset=Article.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ListArticleView(generics.ListAPIView):
    serializer_class = ListArticleSerializer
    authentication_classes = []  # disables authentication
    permission_classes = []

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Article.objects.all()
            return queryset