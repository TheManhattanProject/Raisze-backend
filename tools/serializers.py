from rest_framework import serializers
from .models import Valuation


class CreateValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = ('email','json_data',)
