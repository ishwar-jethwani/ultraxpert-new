import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .api_base_url import *
import json

class MediumView(APIView):
    def get(self,request):
        self.data = request.GET
        self.base_url = MEDIUM_BASE_URL
        if "action" in self.data:
            action = int(self.data.get("action",1))
            action_mapper = {
                1: self.get_all_blogs,
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
            data = requests.get(url=self.base_url)
            self.ctx = {"data": data}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        



