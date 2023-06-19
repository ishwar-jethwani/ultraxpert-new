from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Enterprise, Employee, Training
from .serializers import EnterpriseSerializer, EmployeeSerializer, TrainingSerializer
from datetime import datetime, timedelta


# Create your views here.

class EnterpriseView(APIView):
    """Enterprise View"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        self.data = request.GET
        self.user = request.user
        if 'action' in self.data:
            action = int(self.data['action'])
            action_mapper = {
                1: self.get_enterprise,
                2: self.get_enterprises_list,
                3: self.get_employee_list,
                4: self.get_employee
            }
            action_status = action_mapper.get(action, lambda:"invalid")()
            if action_status == "invalid":
                self.ctx = {"msg": "Invalid Action"}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, status=self.status)
        else:
            return Response({"msg": "Invalid Action"}, status=status.HTTP_400_BAD_REQUEST)

    def get_enterprise(self):
        enterprise_id = self.data.get("enterprise_id")
        try:
            obj = Enterprise.objects.get(id=enterprise_id)
            if obj:
                serialized_data = EnterpriseSerializer(obj)
                self.ctx = {"msg": "Enterprise Profile", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Enterprise Found", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_enterprises_list(self):
        try:
            objs = Enterprise.objects.filter(owner=self.user)
            if objs.exists():
                serialized_data = EnterpriseSerializer(objs, many=True)
                self.ctx = {"msg": "Enterprise List", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Enterprise Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_employee_list(self):
        role = self.data.get("role")
        try:
            objs = Employee.objects.filter(enterprise__owner=self.user)
            if role:
                objs = objs.filter(role=role)
            if objs.exists():
                serialized_data = EmployeeSerializer(objs, many=True)
                self.ctx = {"msg": "Employee List Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Employee Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_employee(self):
        employee_id = self.data.get("employee_id")
        try:
            obj = Employee.objects.get(id=employee_id)
            trainings_objs = obj.training.all()
            if obj:
                trainings = TrainingSerializer(trainings_objs, many=True)
                serialized_data = EmployeeSerializer(obj)
                serialized_data.data.update({"trainings": trainings.data}) 
                self.ctx = {"msg": "Employee Profile", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Employee Found", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.add_enterprise,
                2: self.add_employee
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)


    def add_enterprise(self):
        name = self.data.get("name")
        description = self.data.get("description")
        strength = self.data.get("company_size")
        registered_on = self.data.get("registered_on")
        registration_no = self.data.get("registration_no")
        website_link = self.data.get("website_link")
        try:
            if registered_on:
                registered_on_obj = datetime.strptime(registered_on, "%d/%m/%Y")

            obj = Enterprise(
                owner = self.user,
                name = name,
                description = description,
                strength = strength,
                registered_on = registered_on_obj,
                registration_no = registration_no,
                website_link = website_link
            )
            obj.save()
            self.ctx = {"msg": "Enterprise Profile is Created!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    

    def add_employee(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        dob = self.data.get("dob")
        marital_status = self.data.get("marital_status")
        anniversary_date = self.data.get("anniversary_date")
        gender = self.data.get("gender")
        role = self.data.get("role")
        about_me = self.data.get("about_me")
        enterprise_id = self.data.get("enterprise_id")
        training_id = self.data.get("training_id")
        try:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.dob = dob
            self.user.marital_status = marital_status
            self.user.anniversary_date = anniversary_date
            self.user.gender = gender
            self.user.save()
            enterprise = Enterprise.objects.get(id=enterprise_id)
            training = Training.objects.get(id=training_id)
            obj = Employee(
                user = self.user,
                enterprise = enterprise,
                about_me = about_me,
                role = role,
            )
            obj.save()
            obj.training.add(training)
            self.ctx = {"msg": "Employee Profile is Created!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        


class TrainingView(APIView):
    """Training View"""
    def get(self, request):
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_training,
                2: self.get_trainings_list
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def get_training(self):
        training_id = self.data.get("training_id")
        try:
            obj = Training.objects.get(id=training_id)
            if obj:
                serialized_data = TrainingSerializer(obj)
                self.ctx = {"msg": "Trainings Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Training Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_trainings_list(self):
        technology = self.data.get("technology")
        start_date = self.data.get("start_date")
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        duration = self.data.get("duration")
        price = self.data.get("price")
        try:
            objs = Training.objects.all()
            if technology:
                objs = objs.filter(technology=technology)
            elif start_date:
                start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
                objs = objs.filter(start_date=start_date_obj)
            elif duration:
                objs = objs.filter(duration=duration)
            elif price:
                objs = objs.filter(price=price)
            elif start_time:
                start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
                objs = objs.filter(start_time=start_time_obj)
            elif end_time:
                end_time_obj = datetime.strptime(end_time, "%H:%M:%S")
                objs = objs.filter(end_time=end_time_obj)
            
            if objs.exists():
                serialized_data = TrainingSerializer(objs, many=True)
                self.ctx = {"msg": "Training List Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Training Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    def post(self,request):
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.add_training,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    def add_training(self):
        name = self.data.get("name")
        technology = self.data.get("technology")
        start_date = self.data.get("start_date")
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S")
        duration = self.data.get("duration")
        price = self.data.get("price")
        try:
            obj = Training(
                name = name,
                technology = technology,
                start_time = start_time_obj,
                end_time = end_time_obj,
                start_date = start_date_obj,
                duration = duration,
                price = price
            )
            obj.save()
            self.ctx = {"msg": "Training is Created!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR