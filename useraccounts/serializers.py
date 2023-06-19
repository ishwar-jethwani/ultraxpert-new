from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from experts.models import *

class CustomRegisterSerializer(RegisterSerializer):
    """Serializer For Custom Registration"""
    first_name = serializers.CharField(max_length=60, required=False)
    last_name  = serializers.CharField(max_length=60, required=False)
    reffered_by = serializers.CharField(max_length=10, required=False) 
    mobile = serializers.CharField(max_length=13, required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name")
        data_dict["last_name"] = self.validated_data.get("last_name")
        data_dict["reffered_by"] = self.validated_data.get("reffered_by")
        data_dict["mobile"] = self.validated_data.get("mobile")
        return data_dict
class Userserializer(serializers.ModelSerializer):
    """Serializer for internal user"""
    class Meta:
        fields = ("pk", "first_name", "last_name", "is_verified", "is_expert", "email", "mobile", "refer_code", "reffered_by")
        model = UserAccount


class UserDetailSerializer(serializers.ModelSerializer):
    "Serializer for user details"
    class Meta:
        fields = ("pk", "first_name", "last_name", "gender", "profile_img")
        model = UserAccount
