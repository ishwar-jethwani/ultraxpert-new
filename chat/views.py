from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .models import *
from .serializers import *


class ChatView(APIView):
    """Chat View"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_chat_list,
                2: self.get_chat,
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_chat_list(self):
        try:
            chats = Chat.objects.filter(expert__user=self.user)
            if chats.exists():
                serialized_data = ChatSerializer(chats, many=True)
                self.ctx = {"msg": "Chat List Loaded!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Chat Found!", "data": []}
                self.status = status.HTTP_404_NOT_FOUND
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_chat(self):
        try:
            chat_id = self.data.get("chat_id")
            expert_chat = Chat.objects.get(expert__user=self.user, id=chat_id)
            if expert_chat:
                serialized_data = ChatSerializer(expert_chat)
                self.ctx = {"msg": "Chat List Loaded!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Chat Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

class NotificationView(APIView):
    """Notification View"""
    def get(self,request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_notification_list,
                2: self.get_notification,
            }
            action_status = action_mapper.get(action, lambda:"Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_notification_list(self):
        try:
            notifications = Notification.objects.filter(accepted_by__user=self.user)
            if notifications.exists():
                serialized_data = NotificationSerializer(notifications, many=True)
                self.ctx = {"msg": "Notification List Loaded!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Notification Found!", "data": []}
                self.status = status.HTTP_404_NOT_FOUND
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_notification(self):
        try:
            notification_id = self.data.get("notification_id")
            notification = Notification.objects.get(accepted_by__user=self.user, id=notification_id)
            if notification:
                serialized_data = NotificationSerializer(notification)
                self.ctx = {"msg": "Notification Loaded!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Notification Found!", "data": None}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR