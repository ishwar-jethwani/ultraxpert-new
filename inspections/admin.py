from django.contrib import admin
from .models import *

admin.site.register([Questions, ExpertTestReport, InterviewSchedule, ExpertAnswers])
