from rest_framework import serializers
from .models import *
from users.serializers import UserViewSerializer

class CreateTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id', 'order_id', 'made_by', 'checksum')


class TransactionViewSerializer(serializers.ModelSerializer):
    made_by = UserViewSerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'made_by')