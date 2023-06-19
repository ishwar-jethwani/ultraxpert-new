from rest_framework import serializers
from .models import *
from experts.serializers import ExpertSerializer

class QuestionsSerializer(serializers.ModelSerializer):
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Questions
        fields = ("id", "question", "answer", "topic", "seq_num", "updated_on", "date_created")


class TestReportSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer()
    test_scheduled = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    start_time = serializers.TimeField(format="%H:%M:%S")
    end_time = serializers.TimeField(format="%H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")

    class Meta:
        model = ExpertTestReport
        fields = ("id", "expert", "qualified", "correct_ans", "test_scheduled", "start_time", "end_time", "updated_on", "date_created")

class InterviewScheduleSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer()
    start_time = serializers.TimeField(format="%H:%M:%S")
    end_time = serializers.TimeField(format="%H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    date_created = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")

    class Meta:
        model = InterviewSchedule
        fields = ("id", "expert", "meeting_link", "start_time", "end_time", "updated_on", "date_created")