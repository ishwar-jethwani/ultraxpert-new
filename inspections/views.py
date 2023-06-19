from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *

class QuestionsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        self.user = request.user
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_questions,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def get_questions(self):
        question_filter_topic = self.data.get("topic")
        try:
            questions = Questions.objects.filter(topic=question_filter_topic)
            if questions.exists():
                serializer = QuestionsSerializer(questions, many=True)
                self.ctx = {"msg": "Questions Fetched Successfully", "data": serializer.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Questions Found", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Questions Not Fetched", "error_msg": str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self, request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.post_question,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def post_question(self):
        question = self.data.get("question")
        topic = self.data.get("topic")
        answer = self.data.get("answer")
        options = self.data.get("options")
        count = Questions.objects.count()
        try:
            obj = Questions(
                question=question,
                options=options,
                topic=topic,
                answer=answer,
                seq_num=count+1
            )
            obj.save()
            self.ctx = {"msg": "Question Added Successfully", "data": None}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Question Not Added", "error_msg": str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class AnswerView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.post_answers,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def post_answers(self):
        question_id = self.data.get("question_id")
        answer = self.data.get("answer")
        try:
            question = Questions.objects.filter(id=question_id)
            expert = Expert.objects.get(user=self.user)
            obj = ExpertAnswers(
                expert = expert,
                question=question.first(),
                answer=answer,
            )
            obj.save()
            expert = Expert.objects.get(user=self.user)
            report_obj = ExpertTestReport.objects.get(expert=expert)
            if question.exists():
                if report_obj:
                    if question.first().answer == obj.answer:
                        report_obj.correct_ans+=1
                        report_obj.save()
            self.ctx = {"msg": "Answers Added Successfully", "data": None}
            self.status = status.HTTP_200_OK               
        except Exception as e:
            self.ctx = {"msg": "Answers Not Fetched", "error_msg": str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


class ReportView(APIView):
    def get(self,request):
        self.user = request.user
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_report,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def get_report(self):
        try:
            expert = Expert.objects.get(user=self.user)
            report = ExpertTestReport.objects.get(expert=expert)
            if report:
                if report.correct_ans>=4:
                    report.qualified = True
                    report.save()
                serializer = TestReportSerializer(report)
                self.ctx = {"msg": "Report Fetched Successfully!", "data": serializer.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Report Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Report Not Fetched!", "error_msg": str(e),"data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.post_report,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def post_report(self):
        test_scheduled = self.data.get("test_scheduled")
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = ExpertTestReport(
                expert = expert,
                test_scheduled = test_scheduled,
                start_time = start_time,
                end_time = end_time,
            )
            obj.save()
            self.ctx = {"msg": "Report Added Successfully", "data": None}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Report Not Fetched!", "error_msg": str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class InterviewDetailView(APIView):
    def get(self,request):
        self.user = request.user
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_interview,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_interview(self):
        try:
            expert = Expert.objects.get(user=self.user)
            interview = InterviewSchedule.objects.get(expert=expert)
            if interview:
                serializer = InterviewScheduleSerializer(interview)
                self.ctx = {"msg": "Interview Fetched Successfully!", "data": serializer.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Interview Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Interview Not Fetched!", "error_msg": str(e),"data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.post_interview,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def post_interview(self):
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        meeting_link = self.data.get("meeting_link")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = InterviewSchedule(
                expert = expert,
                start_time = start_time,
                end_time = end_time,
                meeting_link = meeting_link,
            )
            obj.save()
            self.ctx = {"msg": "Interview Added Successfully", "data": None}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Interview Not Fetched!", "error_msg": str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR