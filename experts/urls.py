from django.urls import path
from .views import *

urlpatterns = [ 
    path("", ExpertView.as_view(), name="profile"),
    path("update/", UpdateExpertView.as_view(), name="update_expert"),
    path("services/",ServiceView.as_view(), name="services"),
    path("customers/", CustomerDisplayView.as_view(), name="customer_display"),
    path("followers/", FollowerView.as_view(), name="followers"),
]