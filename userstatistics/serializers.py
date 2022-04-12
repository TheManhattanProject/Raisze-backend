from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FinancialSheets



class CreateFinancialSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSheets
        fields = ('sheets',)

    def create(self, validated_data):
        print(validated_data)
        obj=FinancialSheets(sheet_owner=self.context.get('user'),**validated_data)
        obj.save()
        return obj
