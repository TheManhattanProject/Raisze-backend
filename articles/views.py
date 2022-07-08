from django.forms import ValidationError
from django.http import Http404
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
            queryset = Article.objects.filter(is_deleted=False).order_by("-nor_score")
            return queryset


class UpdateArticlesView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateArticleSerializer
    # authentication_classes = []

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         self.permission_classes = []
    #     return super().get_permissions()

    def get_object(self):
        if self.kwargs.get('id'):
            activity = Article.objects.filter(
                article_id=self.kwargs.get('id'), is_deleted=False)
        else:
            raise ValidationError("Article id was not passed in the url")
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
