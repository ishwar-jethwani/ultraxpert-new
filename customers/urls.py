from django.urls import path,include
from .views import *

urlpatterns = [
    path("experts/", ExpertDisplayView.as_view(), name="experts"),
    path("", CustomerView.as_view(), name="customers"),
    path("services/", ServiceDisplayView.as_view(), name="service_display"),
    path("connect/", ExpertConnectionsView.as_view(), name="connect_expert"),
    path("rating/", RatingView.as_view(), name="ratings"),
    path("query/", QueryView.as_view(), name="query"),
 ]