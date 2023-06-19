from django.urls import path
from .views import *

urlpatterns = [
    path("", BookingView.as_view(), name="book_service")
]