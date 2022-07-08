from rest_framework import serializers
from .models import *

class CreateTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'order_id', 'made_by', 'checksum')