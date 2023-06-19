from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from experts.models import *
from django.core.paginator import Paginator
from experts.serializers import *
from .models import *
from .serializers import *
from django.db.models import Avg


class ExpertDisplayView(APIView):
    """Expert List For Home Page View"""
    def get(self, request):
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_expert_list,
                2: self.get_expert_details,
                3: self.get_top_experts
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_expert_list(self):
        try:
            page_number = self.data.get("page",1)
            experts = Expert.objects.filter(user__is_verified=True)
            default_number = 10
            count = experts.count()
            self.data = []
            if count < default_number:
                default_number = count
            experts = Paginator(experts, default_number)
            experts = experts.page(page_number)
            for expert in experts:
                skills = Skills.objects.filter(expert=expert)
                experience = Experience.objects.filter(expert=expert)
                educations = Education.objects.filter(expert=expert)
                ratings = ExpertRatings.objects.filter(expert=expert)
                ratings_count = ratings.count()
                avg_rating = ratings.aggregate(Avg("ratings"))
                serialized_expert = ExpertSerializer(expert)
                serialized_skills = SkillSerializer(skills, many=True)
                serialized_experience = ExperienceSerializer(experience, many=True)
                serialized_education = EducationSerializer(educations, many=True)
                self.data.append({
                    "expert": serialized_expert.data, 
                    "education": serialized_education.data, 
                    "skills": serialized_skills.data, 
                    "experience": serialized_experience.data ,
                    "avg_ratings": avg_rating,
                    "ratings_count": ratings_count
                    })
            if len(self.data):
                self.ctx = {"msg":"Expert List Loaded Successfully!", "data": self.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Repleted Data Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def get_expert_details(self):
        try:
            expert_id = self.data.get("expert_id")
            expert = Expert.objects.get(id=expert_id)
            expert.profile_view += 1
            expert.save()
            if self.request.user.is_authenticated:
                try:
                    customer = Customer.objects.get(user=self.request.user)
                    obj = RecentlyViewedExpert(
                        customer=customer,
                    )
                    obj.save()
                    obj.experts.add(expert)
                except Exception as e:
                    pass
            expert_skill = Skills.objects.filter(expert=expert)
            expert_experience = Experience.objects.filter(expert=expert)
            expert_education = Education.objects.filter(expert=expert)
            expert_achievements = Achievements.objects.filter(expert=expert)
            expert_ratings = ExpertRatings.objects.filter(expert=expert)
            expert_ratings_count = expert_ratings.count()
            expert_avg_rating = expert_ratings.aggregate(Avg("ratings"))
            serialized_expert = ExpertSerializer(expert).data
            serialized_ratings = RatingsSerializer(expert_ratings, many=True).data
            serialized_achievements = {}
            serialized_skills = {}
            serialized_experience = {}
            serialized_education = {}
            if expert_achievements.exists():
                expert_achievements = expert_achievements.first()
                serialized_achievements = AchievementSerializer(expert_achievements).data
            elif expert_skill.exists():
                expert_skill = expert_skill.first()
                serialized_skills = SkillSerializer(expert_skill).data
            elif expert_experience.exists():
                expert_experience = expert_experience.first()
                serialized_experience = ExperienceSerializer(expert_experience).data
            elif expert_education.exists():
                expert_education = expert_education.first()
                serialized_education = EducationSerializer(expert_education).data
            self.data = {
                    "expert": serialized_expert, 
                    "education": serialized_education, 
                    "skills": serialized_skills, 
                    "experience": serialized_experience,
                    "achievements": serialized_achievements,
                    "avg_ratings": expert_avg_rating,
                    "ratings_count": expert_ratings_count,
                    "ratings": serialized_ratings,
                    }
            if len(self.data):
                self.ctx = {"msg":"Expert Details Loaded Successfully!", "data": self.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Repleted Data Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_top_experts(self):
        try:
            top_experts = Expert.objects.filter(user__is_verified=True).order_by("-profile_view")[:10]
            serialized_data = ExpertSerializer(top_experts, many=True)
            if len(serialized_data.data):
                self.ctx = {"msg":"Top Experts Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Repleted Data Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    
class ServiceDisplayView(APIView):
    """Service Display View"""
    def get(self,request):
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_service_list,
                2: self.get_service_details,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_service_list(self):
        expert_id = self.data.get("expert_id")
        service_name = self.data.get("service_name")
        category_name = self.data.get("category_name")
        duration = self.data.get("duration")
        price = self.data.get("price")
        page_number = self.data.get("page",1)
        try:
            services = Services.objects.all()
            default_number = 10
            count = services.count()
            self.data = []
            if count < default_number:
                default_number = count
            services = Paginator(services, default_number)
            services = services.page(page_number)
            if expert_id:
                services = services.filter(expert__id=expert_id)
            elif service_name:
                services = services.filter(service_name__icontains=service_name)
            elif category_name:
                services = services.filter(category__name__icontains=category_name)
            elif duration:
                services = services.filter(duration=duration)
            elif price:
                services = services.filter(price=price)
            if services.exists():
                serialized_data = ServiceSerializer(services, many=True)
                self.ctx = {"msg":"Service List Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Service List Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_service_details(self):
        service_id = self.data.get("service_id")
        try:
            services = Services.objects.filter(id=service_id)
            if services.exists():
                service = services.first()
                serialized_data = ServiceSerializer(service)
                self.ctx = {"msg":"Service Details Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Service Details Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class CustomerView(APIView):
    """Customer View"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.add_customer,
                2: self.add_customer_interest,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def add_customer(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        dob = self.data.get("dob")
        marital_status = self.data.get("marital_status")
        anniversary_date = self.data.get("anniversary_date")
        gender = self.data.get("gender")
        about_me = self.data.get("about_me")
        profession = self.data.get("profession")
        try:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.dob = dob
            self.user.marital_status = marital_status
            self.user.anniversary_date = anniversary_date
            self.user.gender = gender
            self.user.save()
            obj = Customer(
                user = self.user,
                about_me = about_me,
                profession = profession
            )
            obj.save()
            favorite_obj = FavoriteExpert(
                customer = obj,
            )
            favorite_obj.save()
            self.ctx = {"msg":"Customer Added Successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        

    def add_customer_interest(self):
        try:
            interest_list = self.data.get("interest_list")
            customer = Customer.objects.get(user=self.user)
            obj = CustomerInterest(
                customer = customer,
                interest_list = interest_list
            )
            obj.save()
            self.ctx = {"msg": "Customer interest added successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR   
  

class ExpertConnectionsView(APIView):
    """Customer can follow expert"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_favorite_experts,
                2: self.recently_viewed_experts
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def get_favorite_experts(self):
        try:
            customer = Customer.objects.get(user=self.request.user)
            favorite_experts = FavoriteExpert.objects.get(customer=customer)
            if favorite_experts:
                experts = favorite_experts.experts.all()
                serialized_data = ExpertSerializer(experts, many=True)
                self.ctx = {"msg":"Favorite Experts Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Favorite Experts Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def recently_viewed_experts(self):
        try:
            page_number = self.data.get("page",1)
            customer = Customer.objects.get(user=self.user)
            recently_viewed_experts = RecentlyViewedExpert.objects.get(customer=customer)
            self.data = []
            if recently_viewed_experts:
                experts = recently_viewed_experts.experts.all()
                default_number = 10
                count = experts.count()          
                if count < default_number:
                    default_number = count
                experts = Paginator(experts, default_number)
                experts = experts.page(page_number)
                for expert in experts:
                    skills = Skills.objects.filter(expert=expert)
                    experience = Experience.objects.filter(expert=expert)
                    educations = Education.objects.filter(expert=expert)
                    ratings = ExpertRatings.objects.filter(expert=expert)
                    ratings_count = ratings.count()
                    avg_rating = ratings.aggregate(Avg("ratings"))
                    serialized_expert = ExpertSerializer(expert)
                    serialized_skills = SkillSerializer(skills, many=True)
                    serialized_experience = ExperienceSerializer(experience, many=True)
                    serialized_education = EducationSerializer(educations, many=True)
                    self.data.append({
                        "expert": serialized_expert.data, 
                        "education": serialized_education.data, 
                        "skills": serialized_skills.data, 
                        "experience": serialized_experience.data ,
                        "avg_ratings": avg_rating,
                        "ratings_count": ratings_count
                        })
            if len(self.data):
                self.ctx = {"msg":"Expert List Loaded Successfully!", "data": self.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg":"Recently Viewed Experts Not Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


    def post(self,request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.follow,
                2: self.unfollow,
                3: self.add_favorite,
                4: self.remove_favorite
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    
    def follow(self): 
        expert_id = self.data.get("expert_id")
        try:
            customer = Customer.objects.get(user=self.user)
            expert = Expert.objects.get(id=expert_id)
            obj, created = ExpertFollowers.objects.get_or_create(expert=expert)
            obj.customer.add(customer)
            self.ctx = {"msg": "Successfully Followed!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def unfollow(self):
        expert_id = self.data.get("expert_id")
        try:
            expert = Expert.objects.get(id=expert_id)
            customer = Customer.objects.get(user=self.user)
            obj = ExpertFollowers.objects.get(expert = expert)
            if obj:
                try:
                    obj.customer.remove(customer)
                    self.ctx = {"msg": "Successfully Unfollowed!"}
                    self.status = status.HTTP_200_OK
                except:
                    self.ctx = {"msg": "Not followed by User"}
                    self.status = status.HTTP_404_NOT_FOUND
            else:
                self.ctx = {"msg": "Not followed by User"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def add_favorite(self):
        expert_id = self.data.get("expert_id")
        try:
            expert = Expert.objects.get(id=expert_id)
            customer = Customer.objects.get(user=self.user)
            favorite_expert_obj, create_status = FavoriteExpert.objects.get_or_create(customer=customer)
            favorite_expert_obj.experts.add(expert)
            self.ctx = {"msg": "Expert added in your favorite list successfully!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def remove_favorite(self):
        expert_id = self.data.get("expert_id")
        try:
            expert = Expert.objects.get(id=expert_id)
            customer = Customer.objects.get(user=self.user)
            favorite_expert_obj = FavoriteExpert.objects.get(customer=customer)
            if favorite_expert_obj:
                try:
                    favorite_expert_obj.experts.remove(expert)
                    self.ctx = {"msg": "Expert removed from your favorite list successfully!"}
                    self.status = status.HTTP_200_OK
                except:
                    self.ctx = {"msg": "Expert is not in your favorite list!"}
                    self.status = status.HTTP_400_BAD_REQUEST
            else:
                self.ctx = {"msg": "Expert is not in your favorite list!"}
                self.status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR



class QueryView(APIView):
    """Customer Queries """
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        self.user = request.user
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_queries,
                2: self.get_query_details
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_queries(self):
        try:
            customer = Customer.objects.get(user=self.user)
            queries = CustomerQuery.objects.filter(customer=customer)
            if queries.exists():
                serializer = QuerySerializer(queries, many=True)
                self.ctx = {"msg": "Queries", "data": serializer.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Queries Found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_query_details(self):
        try:
            query_id = self.data.get("query_id")
            customer = Customer.objects.get(user=self.user)
            query = CustomerQuery.objects.get(customer=customer, id=query_id)
            if query:
                serializer = QuerySerializer(query)
                self.ctx = {"msg": "Query Details Loaded Successfully!", "data": serializer.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Query Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1:self.add_queries,
            }
            action_status = action_mapper.get(action,lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def add_queries(self):
        try:
            subject = self.data.get("subject")
            technology_name = self.data.get("technology_name")
            topic = self.data.get("topic")
            description = self.data.get("description")
            customer = Customer.objects.get(user=self.user)
            query =  CustomerQuery(
                customer = customer,
                subject = subject,
                technology_name = technology_name,
                topic = topic,
                description = description
            )
            query.save()
            self.ctx = {"msg": "Query Added Successfully!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class RatingView(APIView):
    """Ratings Views"""
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1:self.post_ratings,
            }
            action_status = action_mapper.get(action,lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    def post_ratings(self):
        try:
            expert_id = self.data.get("expert_id")
            ratings = self.data.get("ratings")
            review = self.data.get("review")
            customer = Customer.objects.get(user=self.user)
            expert = Expert.objects.get(id=expert_id)
            if ratings:
                ratings = int(ratings)
            else:
                ratings = 0
            obj = ExpertRatings(
                expert = expert,
                customer = customer,
                ratings = ratings,
                review = review,
            )
            obj.save()
            self.ctx = {"msg": "Thanks For Ratings!"}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
