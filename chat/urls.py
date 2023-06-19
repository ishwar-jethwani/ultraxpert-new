from django.urls import path
from .views import ChatView, NotificationView

urlpatterns = [
    path("", ChatView.as_view(), name="chat"),
    path("notification/", NotificationView.as_view(), name="notification")
]