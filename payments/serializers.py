from rest_framework import serializers
from .models import *
from useraccounts.serializers import UserDetailSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    amount = serializers.FloatField()
    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1