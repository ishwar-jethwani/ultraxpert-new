from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from django.core.paginator import Paginator


class AuthorView(APIView):
    """Author Create"""
    permission_classes = [permissions.IsAuthenticated]
    # Get Expert Profile
    def get(self, request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data.get("action",1))
            action_mapper = {
                1: self.get_author,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
        
    def get_author(self):
        try:
            author = Author.objects.get(user=self.user)
            
            data_dict = {
                "id": author.pk,
                "profile_img": self.user.profile_img,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "gender": self.user.gender,
                "mobile_number": str(self.user.mobile),
                "email": self.user.email,
                "refer_code": self.user.refer_code,
                "is_verified": self.user.is_verified,
                "is_online": self.user.is_online,
                "profession ": author.profession,
                "about_me": author.about_me
            }
            self.ctx = {"msg": "Author Profile Loaded Successfully!", "data": data_dict}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        

    # Create Author Profile
    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.add_author
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
    def add_author(self):
        first_name = self.data.get("first_name")
        last_name = self.data.get("last_name")
        dob = self.data.get("dob")
        marital_status = self.data.get("marital_status")
        anniversary_date = self.data.get("anniversary_date")
        gender = self.data.get("gender")
        profession = self.data.get("profession")
        about_me = self.data.get("about_me")
        try:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.dob = dob
            self.user.marital_status = marital_status
            self.user.anniversary_date = anniversary_date
            self.user.gender = gender
            self.user.save()
            obj = Author(
                user = self.user,
                about_me = about_me,
                profession = profession
            )
            obj.save()
            self.ctx = {"msg": "Author Profile is Created!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class BlogsView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """Blog View"""
    def get(self,request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data.get("action",1))
            action_mapper = {
                1: self.get_all_blogs,
                2: self.get_all_author_blogs,
                3: self.get_blog_detail,
                4: self.get_categories,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_all_blogs(self):
        try:
            page_number = self.data.get("page",1)
            default_number = 10
            blogs = Blog.objects.all()
            count = blogs.count()
            self.data = []
            if count < default_number:
                default_number = count
            blogs = Paginator(blogs, default_number)
            blogs = blogs.page(page_number)
            serialized_blogs = BlogsSerializer(blogs, many=True)
            self.ctx = {"msg":"Blogs List Loaded Successfully!", "data": serialized_blogs.data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        


    def get_all_author_blogs(self):
        try:
            author_blogs = Blog.objects.filter(author__user=self.user)
            serialize = BlogsSerializer(author_blogs, many=True)
            self.ctx = {"msg": "Blogs Loaded Successfully!", "data": serialize.data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        

    def get_blog_detail(self):
        blog_id = self.data.get("blog_id")
        blog_title = self.data.get("title")
        author = Author.objects.get(user=self.user)
        blogs = Blog.objects.all()
        if blog_id:
            blogs = blogs.filter(id=blog_id, author=author)
        elif blog_title:
            blogs = blogs.filter(title__icontains=blog_title, author=author)
        else:
            self.ctx = {"msg":"Please Provide Blog ID or Title !"}
            self.status = status.HTTP_400_BAD_REQUEST
        try:
            if blogs.exists():
                blog = blogs.first()
                blog_views = BlogView.objects.filter(blog=blog).count()
                pub_date = blog.date_created.strftime("%d-%b-%Y")
                pub_time = blog.date_created.strftime("%H:%M:%S")
                previous_post_id = None
                next_post_id = None
                parent_category_name = ""
                if blog.previous_post is not None:
                    previous_post_id = blog.previous_post.id   
                elif blog.next_post is not None:
                    next_post_id = blog.next_post.id 
                elif blog.category.parent_category is not None:
                     parent_category_name =  blog.category.parent_category.name
                data_dict = {
                    "id":blog.id,
                    "author": {
                        "id":author.id,
                        "first_name": self.user.first_name,
                        "last_name": self.user.last_name,
                        "profession": author.profession,
                        },
                    "blog_category":{
                        "category": blog.category.name,
                        "parent_category": parent_category_name,
                    },
                    "title": blog.title,
                    "content": blog.content,
                    "service_link_list": blog.service_link_list,
                    "images_list": blog.images,
                    "previous_post": previous_post_id,
                    "next_post": next_post_id,
                    "total_comments_count": blog.comment_count,
                    "total_blog_views": blog_views,
                    "publish_date": pub_date,
                    "publish_time": pub_time,  
                }
                self.ctx = {"msg": "Blog Data Loaded Successfully!", "data": data_dict}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Blog Details Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_categories(self):
        try:
            categories = BlogCategory.objects.all()
            serialize = CategorySerializer(categories, many=True)
            self.ctx = {"msg":"Category Loaded Successfully!", "data": serialize.data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR


    def post(self,request):
        self.data = request.data
        self.user = request.user
        if "action" in request.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.add_blog_category,
                2: self.post_blog,
                3: self.update_blog,
                4: self.delete_blog
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def add_blog_category(self):
        name = self.data.get("category_name")
        cate_img = self.data.get("img_url")
        number = BlogCategory.objects.all().count()+1
        parent_category_id = self.data.get("parent_category_id")
        try:
            if parent_category_id:
                parent_category = BlogCategory.objects.get(id=parent_category_id)
                obj = BlogCategory(
                    name = name,
                    img = cate_img,
                    number = number,
                    parent_category = parent_category
                )
            else:
                  obj = BlogCategory(
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

    
    def post_blog(self):
        try:
            title = self.data.get("blog_title")
            category_id = self.data.get("category_id")
            content = self.data.get("content")
            service_link_list = self.data.get("service_link_list")
            image_list = self.data.get("image_url_list")
            previous_post_id = self.data.get("previous_post_id")
            next_post_id = self.data.get("next_post_id")
            author = Author.objects.get(user=self.user)
            category = BlogCategory.objects.get(id=category_id)
            previous_post = None
            next_post = None
            if previous_post_id:
                previous_post = Blog.objects.get(id=previous_post_id)
            elif next_post_id: 
                next_post = Blog.objects.get(id=next_post_id)
            obj = Blog(
                author = author,
                title = title,
                content = content,
                category = category,
                previous_post = previous_post,
                next_post = next_post,
                service_link_list = service_link_list,
                images = image_list,
            )
            obj.save()
            self.ctx = {"msg": "Blog Posted Successfully!"}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_blog(self):
        try:
            blog_id = self.data.get("id")
            title = self.data.get("blog_title")
            content = self.data.get("content")
            service_link_list = self.data.get("service_link_list")
            image_list = self.data.get("image_url_list")
            previous_post_id = self.data.get("previous_post_id")
            next_post_id = self.data.get("next_post_id")
            category_id = self.data.get("category_id")
            author = Author.objects.get(user=self.user)
            previous_post = None
            next_post = None
            category = BlogCategory.objects.get(id=category_id)
            if previous_post_id:
                previous_post = Blog.objects.get(id=previous_post_id)
            elif next_post_id: 
                next_post = Blog.objects.get(id=next_post_id)
            obj = Blog.objects.filter(id=blog_id, author=author)
            if obj.exists():
                obj.update(
                    title = title,
                    content = content,
                    category = category,
                    previous_post = previous_post,
                    next_post = next_post,
                    service_link_list = service_link_list,
                    images = image_list,
                )
                self.ctx = {"msg": "Blog Updated Successfully!"}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Blog Object Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def delete_blog(self):
        try:
            blog_id = self.data.get("blog_id")
            obj = Blog.objects.filter(id=blog_id, author__user=self.user)
            if obj.exists():
                obj.delete()
                self.ctx = {"msg": "Blog Deleted Successfully!"}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "Blog Object Not Found!"}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
