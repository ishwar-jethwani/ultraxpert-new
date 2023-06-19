from django.urls import path
from .views import *

urlpatterns = [
    path("", WalletView.as_view(), name="wallet")
]
