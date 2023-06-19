from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, permissions
from customers.serializers import CustomerSerializer, CustomerInterestSerializer
from django.core.paginator import Paginator
from customers.models import Customer, CustomerInterest



class ExpertView(APIView):
    """Expert Create"""
    permission_classes = [permissions.IsAuthenticated]
    # Get Expert Profile
    def get(self, request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data.get("action",1))
            action_mapper = {
                1: self.read_profile,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def read_profile(self):
        try:
            expert = Expert.objects.get(user=self.user)
            profile_view = expert.profile_view
            education = Education.objects.get(expert=expert)
            skills = Skills.objects.get(expert=expert)
            experience = Experience.objects.get(expert=expert)
            try:
                achievements = Achievements.objects.get(expert=expert).achievements
                followers_count = ExpertFollowers.objects.filter(expert=expert).count()
            except Exception as e:
                achievements = "Achievements Not Found"
                followers_count = 0

            data_dict = {
                "id": expert.pk,
                "profile_img": self.user.profile_img,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "gender": self.user.gender,
                "profession": expert.profession,
                "about_me": expert.about_me,
                "mobile_number": str(self.user.mobile),
                "email": self.user.email,
                "refer_code": self.user.refer_code,
                "is_verified": self.user.is_verified,
                "is_online": self.user.is_online,
                "education": education.education,
                "skills": skills.skills_json,
                "experience": experience.experience,
                "achievements": achievements,
                "followers_count": followers_count,
                "profile_view_count": profile_view,
            }
            self.ctx = {"msg": "Profile Loaded Successfully!", "data": data_dict}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Create Expert Profile
    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.create_profile,
                2: self.add_education,
                3: self.add_skills,
                4: self.add_experience,
                5: self.add_bank_details
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def create_profile(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        dob = self.data.get("dob")
        marital_status = self.data.get("marital_status")
        anniversary_date = self.data.get("anniversary_date")
        gender = self.data.get("gender")
        level = self.data.get("level")
        is_expert = self.data.get("is_expert")
        about_me = self.data.get("about_me")
        profession = self.data.get("profession")
        try:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.dob = dob
            self.user.marital_status = marital_status
            self.user.anniversary_date = anniversary_date
            self.user.gender = gender
            self.user.is_expert = is_expert
            self.user.save()
            obj = Expert(
                user = self.user,
                about_me = about_me,
                profession = profession,
                level = level
            )
            obj.save()
            self.ctx = {"msg": "Profile is Created!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def add_education(self):
        education_json = self.data.get("education_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Education(
                expert = expert,
                education = education_json
                )
    
            obj.save()
            self.ctx = {"msg": "Education Added!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def add_skills(self):
        skill_json = self.data.get("skill_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Skills(
                expert = expert,
                skills_json = skill_json
                )
            obj.save()
            self.ctx = {"msg": "Skills Added!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def add_experience(self):
        experience_json = self.data.get("experience_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Experience(
                expert = expert,
                experience = experience_json,
            )
            obj.save()
            self.ctx = {"msg": "Experience Added!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def add_bank_details(self):
        account_holder = self.data.get("account_holder")
        bank_name = self.data.get("bank_name")
        account_number = self.data.get("account_number")
        ifsc_code = self.data.get("ifsc_code")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = BankDetail(
                expert = expert,
                account_holder = account_holder,
                bank_name = bank_name,
                account_number = account_number,
                ifsc_code = ifsc_code
            )
            obj.save()
            self.ctx = {"msg": "Bank Details Added!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class UpdateExpertView(APIView):
    """Update Expert"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.update_profile,
                2: self.update_expert_profile,
                3: self.update_education,
                4: self.update_skills,
                5: self.update_experience,
                6: self.update_bank_details
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def update_profile(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        gender = self.data.get("gender")
        is_expert = self.data.get("is_expert")
        try:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.gender = gender
            self.user.is_expert = is_expert
            self.user.save()
            self.ctx = {"msg":"Profile Updated Successfully!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_expert_profile(self):
        level = self.data.get("level")
        about_me = self.data.get("about_me")
        profession = self.data.get("profession")
        try:
            obj = Expert.objects.filter(user=self.user)
            if obj.exists():
                obj.update(
                    level = level,
                    about_me = about_me,
                    profession = profession
                    )
                self.ctx = {"msg": "Expert profile updated successfully!"}
                self.status = status.HTTP_200_OK    
            else:
                self.ctx = {"msg": "Expert not found !"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_education(self):
        education_json = self.data.get("education_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Education.objects.filter(expert=expert)
            if obj.exists():
                obj.update(
                    education = education_json
                    )
                self.ctx = {"msg": "Education updated successfully!"}
                self.status = status.HTTP_200_OK   
            else:
                self.ctx = {"msg": "Education not found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_skills(self):
        skill_json = self.data.get("skill_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Skills.objects.filter(expert=expert)
            if obj.exists():
                obj.update(
                    skills_json = skill_json
                    )
                self.ctx = {"msg": "Skills updated successfully!"}
                self.status = status.HTTP_200_OK 
            else:
                self.ctx = {"msg": "Skills not found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_experience(self):
        experience_json = self.data.get("experience_json")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = Experience.objects.filter(expert=expert)
            if obj.exists():
                obj.update(
                    experience = experience_json
                )
                self.ctx = {"msg": "Experience updated successfully!"}
                self.status = status.HTTP_200_OK 
            else:
                self.ctx = {"msg": "Experience not found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_bank_details(self):
        account_holder = self.data.get("account_holder")
        bank_name = self.data.get("bank_name")
        account_number = self.data.get("account_number")
        ifsc_code = self.data.get("ifsc_code")
        try:
            expert = Expert.objects.get(user=self.user)
            obj = BankDetail.objects.filter(expert=expert)
            if obj.exists():
                obj.update(
                    account_holder = account_holder,
                    bank_name = bank_name,
                    account_number = account_number,
                    ifsc_code = ifsc_code
                )
                self.ctx = {"msg": "Bank detail updated successfully!"}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Bank details not found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


class ServiceView(APIView):
    """Services API VIew"""
    permission_classes = [permissions.IsAuthenticated]
    # Get Services
    def get(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_expert_services,
                2: self.get_service_category
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_expert_services(self):
        service_id = self.data.get("service_id")
        service_name = self.data.get("service_name")
        try:
            expert = Expert.objects.get(user=self.user)
            services = Services.objects.filter(expert=expert)
            if service_id:
                services = services.filter(id=service_id)
            elif service_name:
                services = services.filter(service_name__icontains=service_name)
            if services.exists():
                serialized_services = ServiceSerializer(services, many=True)
                self.ctx = {"msg": "Data Found Successfully!", "data": serialized_services.data} 
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Data Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND 
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_service_category(self):
        category_id = self.data.get("category_id")
        category_name = self.data.get("category_name")
        try:
            if category_id:
                category = Category.objects.filter(id=category_id)
                if category.exists():
                    serialized_category = CategorySerializer(category, many=True)
                    self.ctx = {"msg": "Data Found Successfully!", "data": serialized_category.data}
                    self.status = status.HTTP_200_OK
                else:
                    self.ctx = {"msg": "Data Not Found!", "data": None}
                    self.status = status.HTTP_404_NOT_FOUND
            elif category_name:
                category = Category.objects.filter(name=category_name)
                if category.exists():
                    serialized_category = CategorySerializer(category, many=True)
                    self.ctx = {"msg": "Data Found Successfully!", "data": serialized_category.data}
                    self.status = status.HTTP_200_OK
                else:
                    self.ctx = {"msg": "Data Not Found!", "data": None}
                    self.status = status.HTTP_404_NOT_FOUND
            else:
                self.ctx = {"msg": "Please Provide Name Or ID for getting category"}
                self.status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR 



    # Create and update service
    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.create_service,
                2: self.update_service,
                3: self.delete_service,
                4: self.create_category,
                5: self.create_time_slot,
                6: self.update_time_slot,
                7: self.delete_time_slot,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    def create_service(self):
        service_name = self.data.get("service_name")
        service_img = self.data.get("service_img")
        category_pk = self.data.get("category")
        description = self.data.get("description")
        duration = self.data.get("duration")
        price = self.data.get("price")
        currency = self.data.get("currency")
        tags = self.data.get("tags_list")
        try:
            category = Category.objects.get(pk=category_pk)
            expert = Expert.objects.get(user=self.user)
            obj = Services(
                expert = expert,
                service_name = service_name,
                service_img = service_img,
                category = category,
                description = description,
                duration = duration,
                price = price,
                currency = currency,
                tags = tags
            )
            obj.save()
            self.ctx = {"msg": "Service Created Successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_service(self):
        service_id = self.data.get("service_id")
        service_name = self.data.get("service_name")
        service_img = self.data.get("service_img")
        category_pk = self.data.get("category")
        description = self.data.get("description")
        duration = self.data.get("duration")
        price = self.data.get("price")
        currency = self.data.get("currency")
        tags = self.data.get("tags_list")
        try:
            category = Category.objects.get(pk=category_pk)
            expert = Expert.objects.get(user=self.user)
            service = Services.objects.filter(expert=expert, pk=service_id)
            if service.exists():
                service.update(
                service_name = service_name,
                service_img = service_img,
                category = category,
                description = description,
                duration = duration,
                price = price,
                currency = currency,
                tags = tags 
                )
                self.ctx = {"msg": "Service Updated Successfully!"}
                self.status = status.HTTP_200_OK 
            else:
                self.ctx = {"msg": "Service Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND 
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


    def delete_service(self):
        service_id = self.data.get("service_id")
        try:
            expert = Expert.objects.get(user=self.user)
            service = Services.objects.filter(expert=expert, pk=service_id)
            if service.exists():
                service.delete()
                self.ctx = {"msg": "Service Deleted Successfully!"}
                self.status = status.HTTP_200_OK 
            else:
                self.ctx = {"msg": "Service Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND 

        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def create_category(self):
        name = self.data.get("category_name")
        cate_img = self.data.get("img_url")
        number = Category.objects.all().count()+1
        parent_category_id = self.data.get("parent_category_id")
        try:
            if parent_category_id:
                parent_category = Category.objects.get(id=parent_category_id)
                obj = Category(
                    name = name,
                    img = cate_img,
                    number = number,
                    parent_category = parent_category
                )
            else:
                  obj = Category(
                    name = name,
                    img = cate_img,
                    number = number
                )
            obj.save()
            self.ctx = {"msg": "Category Created Successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def create_time_slot(self):
        service_id = self.data.get("service_id")
        notify_before = self.data.get("notify_before")
        notify_before_time = self.data.get("notify_before_time")
        notify_after = self.data.get("notify_after")
        notify_after_time = self.data.get("notify_after_time")
        day = self.data.get("day")
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        timezone = self.data.get("timezone")
        duration = int(self.data.get("duration"))
        try:
            expert = Expert.objects.get(user=self.user)
            service = Services.objects.get(id=service_id)
            event_obj = Event(
                expert = expert,
                service = service,
                notify_before = notify_before,
                notify_before_time = notify_before_time,
                notify_after = notify_after,
                notify_after_time = notify_after_time
            )
            event_obj.save()
            event_schedule_obj = EventSchedule(
                day = day,
                event = event_obj
            )
            event_schedule_obj.save()
            event_schedule_time_obj = EventScheduleTime(
                schedule = event_schedule_obj,
                start_time = start_time,
                end_time = end_time,
                timezone = timezone,
                duration = duration,
            )
            event_schedule_time_obj.save()
            self.ctx = {"msg": "Time Slot Created Successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_time_slot(self):
        time_slot_id = self.data.get("time_slot_id")
        notify_before = self.data.get("notify_before")
        notify_before_time = self.data.get("notify_before_time")
        notify_after = self.data.get("notify_after")
        notify_after_time = self.data.get("notify_after_time")
        day = self.data.get("day")
        start_time = self.data.get("start_time")
        end_time = self.data.get("end_time")
        timezone = self.data.get("timezone")
        duration = int(self.data.get("duration"))
        try:
            event_obj = Event.objects.get(id=time_slot_id)
            event_obj.notify_before = notify_before
            event_obj.notify_before_time = notify_before_time
            event_obj.notify_after = notify_after
            event_obj.notify_after_time = notify_after_time
            event_obj.save()
            event_schedule_obj = EventSchedule.objects.get(event=event_obj)
            event_schedule_obj.day = day
            event_schedule_obj.save()
            event_schedule_time_obj = EventScheduleTime.objects.get(schedule=event_schedule_obj)
            event_schedule_time_obj.start_time = start_time
            event_schedule_time_obj.end_time = end_time
            event_schedule_time_obj.timezone = timezone
            event_schedule_time_obj.duration = duration
            event_schedule_time_obj.save()
            self.ctx = {"msg": "Time Slot Updated Successfully!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delete_time_slot(self):
        time_slot_id = self.data.get("time_slot_id")
        try:
            event_obj = Event.objects.get(id=time_slot_id)
            event_obj.delete()
            self.ctx = {"msg": "Time Slot Deleted Successfully!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


class CustomerDisplayView(APIView):
    """customer List For Home Page View"""
    def get(self,request):
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_customer_list,
                2: self.get_customer_detail,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg":"Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data":None}, status.HTTP_400_BAD_REQUEST)
    
    def get_customer_list(self):
        try:
            page = self.data.get("page",1)
            customers_interest = CustomerInterest.objects.filter(customer__user__is_verified=True)
            default_number = 10
            count = customers_interest.count()
            if count < default_number:
                default_number = count
            customers_interest = Paginator(customers_interest, default_number)
            customers_interest = customers_interest.page(page)
            serialized_data = CustomerInterestSerializer(customers_interest, many=True)
            self.ctx = {"msg": "Customers Data Loaded Successfully", "data": serialized_data.data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def get_customer_detail(self):
        try: 
            customer_id = self.data.get("customer_id")
            customers = Customer.objects.filter(user__is_verified=True,id=customer_id)
            if customers.exists():
                customer = customers.first()
                interest = CustomerInterest.objects.get(customer=customer)
                serialized_data = CustomerInterestSerializer(interest)
                self.ctx = {"msg": "Customer Detail Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Customer Details Not Found"}
                self.status = status.HTTP_404_NOT_FOUND 
        except Exception as e:    
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR  


        
class FollowerView(APIView):
    """Get Follower of Experts"""   
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_follower_list,
                2: self.get_follower_detail,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg":"Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data":None}, status.HTTP_400_BAD_REQUEST)
    
    def get_follower_list(self):
        try:
            page = self.data.get("page",1)
            expert = Expert.objects.get(user=self.user)
            followers = ExpertFollowers.objects.get(expert=expert)
            followers = followers.customer.all()
            default_number = 10
            count = followers.count()
            if count < default_number:
                default_number = count
            followers = Paginator(followers, default_number)
            followers = followers.page(page)
            serialized_data = CustomerSerializer(followers, many=True)
            self.ctx = {"msg": "Followers Data Loaded Successfully", "data": serialized_data.data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_follower_detail(self):
        try: 
            customer_id = self.data.get("customer_id")
            expert = Expert.objects.get(user=self.user)
            followers = ExpertFollowers.objects.get(expert=expert)
            followers = followers.customer.all()
            follower = followers.get(id=customer_id)
            if follower:
                serialized_data = CustomerSerializer(follower)
                self.ctx = {"msg": "Customer Detail Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Customer Details Not Found"}
                self.status = status.HTTP_404_NOT_FOUND 
        except Exception as e:    
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR