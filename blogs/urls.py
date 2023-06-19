from django.urls import path
from .views import *

urlpatterns = [
    path("author/", AuthorView.as_view(), name="author"),
    path("", BlogsView.as_view(), name="blogs")
]
