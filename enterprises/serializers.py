from rest_framework import serializers
from .models import *
from useraccounts.serializers import UserDetailSerializer

class EnterpriseSerializer(serializers.ModelSerializer):
    owner = UserDetailSerializer()
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_updated = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    registered_on = serializers.DateField(format="%d-%b-%Y")
    class Meta:
        model = Enterprise
        fields = "__all__"
        depth = 1


class TrainingSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format="%d-%b-%Y")
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_updated = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Training
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    enterprise = EnterpriseSerializer()
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_updated = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Employee
        fields = ("id", "user", "enterprise", "role", "about_me", "date_created", "date_updated")
        depth = 1
