from rest_framework import serializers
from .models import *
from useraccounts.serializers import UserDetailSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    created_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Customer
        fields = ("id", "user", "profession", "updated_on", "created_on")

class QuerySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = CustomerQuery
        fields = ("id", "customer", "subject", "technology_name", "topic", "description", "medium", "status", "date_created", "updated_on")

class CustomerInterestSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = CustomerInterest
        fields = ("id", "customer", "interest_list", "updated_on", "date_created")
        depth = 1
    
    
