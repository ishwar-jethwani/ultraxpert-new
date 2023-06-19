from django.urls import path
from .views import *    


urlpatterns = [
    path("", EnterpriseView.as_view(), name="enterprises"),
    path("trainings/", TrainingView.as_view(), name="trainings"),


    
]