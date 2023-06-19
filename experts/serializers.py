from rest_framework.serializers import ModelSerializer
from .models import *
from useraccounts.serializers import *



class ExpertSerializer(ModelSerializer):
    """Expert Serializer for showing json response"""
    user = UserDetailSerializer()
    created_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Expert
        fields = ("id", "user", "profession", "about_me",  "updated_on", "created_on")
        depth = 1

class SkillSerializer(ModelSerializer):
    """Skill Serializer for showing json response"""
    class Meta:
        model = Skills
        fields = ("id", "skills_json")

class EducationSerializer(ModelSerializer):
    """Education Serializer for showing json response"""
    class Meta:
        model = Education
        fields = ("id", "education")

class ExperienceSerializer(ModelSerializer):
    """Experience Serializer for showing json response"""
    class Meta:
        model = Experience
        fields = ("id", "experience")

class AchievementSerializer(ModelSerializer):
    """Achievement Serializer for showing json response"""
    class Meta:
        model = Achievements
        fields = ("id", "achievements")


class RatingsSerializer(ModelSerializer):
    """Rating Serializer for showing json response"""
    class Meta:
        model = ExpertRatings
        fields = ("id", "ratings", "review")



class CategorySerializer(ModelSerializer):
    """Category Serializer for showing json response"""
    class Meta:
        model = Category
        fields = ("id", "name")


class ServiceSerializer(ModelSerializer):
    """Services Serializer for showing json response"""
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")   
    category = CategorySerializer()
    class Meta:
        model = Services
        fields = ("id", "service_name", "service_img", "description", "category", "duration", "price", "currency", "tags", "updated_on", "date_created")

