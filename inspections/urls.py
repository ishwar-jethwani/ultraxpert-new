from django.urls import path
from .views import *

urlpatterns = [ 
    path("questions/", QuestionsView.as_view(), name="questions"),
    path("answer/", AnswerView.as_view(), name="answer"),
    path("report/", ReportView.as_view(), name="report"),
    path("interview/", InterviewDetailView.as_view(), name="interview"),
]