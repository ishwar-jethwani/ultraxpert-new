from rest_framework.serializers import ModelSerializer
from .models import *


class BlogsSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ("id", "title")
class CategorySerializer(ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ("name", "img", "number"," parent_category")
        depth = 1
