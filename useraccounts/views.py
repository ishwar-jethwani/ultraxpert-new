from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import get_template
from django.core.mail import send_mail
from django.middleware import csrf
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from useraccounts.serializers import Userserializer
from django.conf import settings
import random
from .models import *
from rest_framework.parsers import FileUploadParser,ParseError
from help_function.aws_main import AWSServices
from django.db.models import Q
from help_function.main import MessageHandling
from django.conf import settings
import jwt


def home(request):
    return render(request,"base.html")

class LoginView(APIView):
    """Main Login View"""

    def get(self, request):
        try:
            self.data = request.GET
            email = self.data.get("email")
            mobile = self.data.get("mobile")
            self.get_otp(email=email, mobile=mobile)
            return Response({"msg":"Sent OTP"})
        except Exception as e:
            return Response({"msg":"Not Sent OTP", "error_msg": str(e)})

    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    def get_user(self,user):
        serialize = Userserializer(user)
        return serialize.data

    def get_otp(self, email=None, mobile=None ):
        gen_otp = random.randint(100000,999999)
        user_account = UserAccount.objects.get(Q(email=email) | Q(mobile=mobile))
        user_account.user_otp = gen_otp
        user_account.save()
        send_mail(
            from_email = None,
            recipient_list = [email],
            subject = "UltraCreation Verification OTP",
            # html_message = htmly,
            message = f"Please put the otp {gen_otp} for login"
            )
        return (gen_otp,user_account)
        
    def get_response(self, user):
        original_response = self.response
        mydata = self.get_user(user)
        original_response.data.update(mydata)
        email = mydata["email"]
        # username = mydata["username"]
        subject = "Ultra Creation Sending Email"
        message = "Hi %s! Welcome to UltraXpert" % email
        # htmly = get_template("welcome-email.html")
        # htmly = htmly.render({"username":username})
        send_mail(
            from_email = None,
            recipient_list = [email],
            subject =subject,
            # html_message = htmly,
            message = message
            )

        return original_response


    def post(self, request, format=None):
        data = request.data
        self.response = Response()        
        email = data.get("email")
        password = data.get("password")
        mobile = data.get("mobile")
        otp = data.get("otp")
        user = None
        if mobile or email or email and password:
            if otp:
                user_account = UserAccount.objects.filter(Q(email=email)|Q(mobile=mobile))
                if user_account.first().user_otp == otp:
                    user = user_account.first()
                else:
                    return Response({"msg":"OTP is not correct"})
            else:
                user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = self.get_tokens_for_user(user)
                self.response.set_cookie(
                    key = settings.SIMPLE_JWT["AUTH_COOKIE"], 
                    value = data["access"],
                    expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure = settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite = settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
                )
                csrf.get_token(request)
                self.response.data = ({"msg": "Login successfully!", "access_token": data["access"], "refresh_token": data["refresh"]})
                return self.get_response(user)
            else:
                return Response({"msg": "This account is not active!"}, status.HTTP_404_NOT_FOUND)
        else:
            return Response({"msg": "Invalid username or password!"}, status.HTTP_404_NOT_FOUND)


# forgot password
class ResetPassword(APIView):
    """Forgot PassWord"""
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        self.email = request.GET.get("email")
        self.user = UserAccount.objects.get(email=self.email)
        if self.user:
            email = self.user.email
            if self.email == email:
                # html = get_template("reset.html")
                # html_data = html.render({"otp":self.gen_otp})
                send_mail(
                from_email = None,
                recipient_list = [email],
                subject ="Reset Your Password",
                # html_message=html_data,
                message = f"This is you otp:{self.gen_otp} to reset your password"
                )
                return Response({"msg":"Email has been sent!"}, status=status.HTTP_200_OK)
            return Response({"msg":"Email is failed to send!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"msg":"You are not in our database!"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        data = request.data
        self.email = data.get("email")
        otp = data.get("otp")
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        self.user = UserAccount.objects.get(email=self.email)
        if self.user.email == self.email:
            if str(otp) == str(self.gen_otp):
                if password == password_confirm:
                    self.user.set_password(password)
                    self.user.save()
                    return Response({"msg":"Password is set successfully!"}, status.HTTP_200_OK)
            return Response({"msg":"You have entered wrong otp!"}, status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    """File Upload view"""
    parser_class = [FileUploadParser]
    # image upload function
    def post(self, request, format=None):
        aws_service = AWSServices()
        if "file" not in request.data:
            raise ParseError("FIle should be provided")
        file_obj = request.data["file"]
        filename = request.data["filename"]
        folder_name = request.data["folder_name"]
        try:
            url = aws_service.file_upload(file=file_obj, filename=filename, folder_name=folder_name)
            return Response({"msg": "File Uploaded Successfully!", "data": {"url": url, "folder_name": folder_name}}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": "Something went wrong !","error_msg": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
           
class VerificationView(APIView):
    """Email and mobile verification api"""
    gen_otp = random.randint(100000,999999)
    def get(self,request):
        self.data = request.GET
        if "action" in self.data:
            action = int(self.data.get("action",1))
            action_mapper = {
                1: self.email_otp_sent,
                2: self.email_verify
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def email_otp_sent(self):
        try:
            email = self.data.get("email")
            user  = UserAccount.objects.filter(email=email)
            if user.exists():
                self.ctx = {"msg":"Email is already registered!"}
                self.status = status.HTTP_400_BAD_REQUEST
            else:
                save_email = UserEmails(email=email, otp=self.gen_otp)
                save_email.save()
                send_mail(
                    from_email = None,
                    recipient_list = [email],
                    subject ="Email Verification",
                    # html_message=html_data,
                    message = f"This is you otp:{self.gen_otp} to verify email"
                    )
                self.ctx = {"msg":"Email has been sent!"}
                self.status = status.HTTP_200_OK

        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def email_verify(self):
        try:
            email = self.data.get("email")
            otp = self.data.get("otp")
            user  = UserEmails.objects.filter(email=email)
            if user.exists():
                if user.first().otp == int(otp):
                    user.update(is_verified=True)
                    self.ctx = {"msg":"Email is verified!"}
                    self.status = status.HTTP_200_OK
                else:
                    self.ctx = {"msg":"You have entered wrong otp!"}
                    self.status = status.HTTP_400_BAD_REQUEST
            else:
                self.ctx = {"msg":"You are not in our database!"}
                self.status = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
