from rest_framework import serializers
from .models import *


class CreateValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = ('email','json_data',)


class CreateToolCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ToolCategory
        fields = ('category_id',)


class CreateToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ('tool', 'attributes', 'category')
        read_only_fields = ('category',)


class UpdateToolsSerializer(serializers.ModelSerializer):
    category = CreateToolCategorySerializer(many=True)

    class Meta:
        model = Tools
        fields = ('tool', 'attributes', 'category')
        read_only_fields = ('category',)
