from django.urls import path
from .views import *

urlpatterns = [
    path("medium/", MediumView.as_view(), name="medium_api")
    
]