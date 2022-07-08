from rest_framework import serializers
from .models import Article

class CreateArticleSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model=Article
        exclude=['created_by']
        
    def create(self, validated_data):
        owner=self.context.get('user')
        post=Article.objects.create(created_by=owner,**validated_data)
        return post

class ListArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields="__all__"