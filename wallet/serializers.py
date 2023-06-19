from rest_framework import serializers
from .models import *

class TransactionSerializer(serializers.ModelSerializer):
    updated_on = serializers.DateTimeField("%d-%b-%Y, %H:%M:%S")
    created_on = serializers.DateTimeField("%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Transaction
        fields = ("wallet", "transaction_balance", "credit", "updated_on", "created_on")
