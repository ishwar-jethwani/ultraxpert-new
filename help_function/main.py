import json
import random
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from rest_framework.response import Response
from rest_framework import status

class FileHandling: 
    """This class will help for sending dict or list from json files"""
    def __init__(self,file_path,changed_data=None):
        self.file_path = file_path
        self.changed_data = changed_data

    def get_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        return data

    def write_data(self):
        with open(self.file_path,"w",encoding="utf-8") as file:
            data = json.dumps(self.changed_data)
            file.write(data)
        return print("Data Added Successfully!")

class MessageHandling:
    def __init__(self, **data):
        self.subject = data.get("subject")
        self.message = data.get("message")
        self.html = data.get("html")
        self.email = data.get("email")
        self.mobile = data.get("mobile")
        self.email_list = data.get("email_list")
        if "action_list" in data:
            actions = data.get("action_list")
            for action in actions:
                action = int(action)
                action_mapper = {
                    1: self.send_email,
                    2: self.send_message,
                    3: self.send_multiple_email
                }
                action_status = action_mapper.get(action, lambda: "Invalid")()
                if action_status == "Invalid":
                    self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                    self.status = status.HTTP_400_BAD_REQUEST
                return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def send_email(self):
        if self.subject and self.message and self.email :
            try:
                send_mail(
                    from_email = None,
                    subject = self.subject,
                    message = self.message,
                    html_message = self.html,
                    recipient_list = [self.email]            
                )
                self.ctx = {"msg": "Email has been sent!"}
                self.status = status.HTTP_200_OK
            except Exception as e:
                self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
                self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            self.ctx = {"msg": "Please provide required arguments"}
            self.status = status.HTTP_400_BAD_REQUEST

    def send_message(self):
        pass

    def send_multiple_email(self):
        if self.email_list and self.subject and self.message:
            try:
                send_mass_mail(
                    subject = self.subject,
                    message = self.message,
                    html_message = self.html,
                    recipient_list = self.email_list
                )
                self.ctx = {"msg": "Email has been sent!"}
                self.status = status.HTTP_200_OK
            except Exception as e:
                self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
                self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            self.ctx = {"msg": "Please provide required arguments"}
            self.status = status.HTTP_400_BAD_REQUEST
            

class Meeting:
    """Meeting Link Generation"""
    def __init__(self):
        self.meeting_code = random.randint(100000,999999)
    def get_meeting_link(self, expert_name):
        self.endpoint = f"{expert_name}/{self.endpoint}" 
        
         
        
        

    
            




