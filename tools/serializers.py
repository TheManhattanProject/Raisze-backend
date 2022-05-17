from rest_framework import serializers
from .models import Valuation
from .models import Tools


class CreateValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = ('email','json_data',)


class CreateToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = ('tool', 'attributes',)
