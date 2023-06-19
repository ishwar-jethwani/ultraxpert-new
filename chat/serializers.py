from rest_framework import serializers
from .models import *
from customers.serializers import CustomerSerializer,QuerySerializer

class MessageSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Message
        fields = ("id", "sent_message", "received_message", "created_on", "updated_on")

class ChatSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    messages = MessageSerializer(many=True)
    created_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Chat
        fields = ("id", "customer", "messages", "created_on", "updated_on")
        depth = 1

class NotificationSerializer(serializers.ModelSerializer):
    query = QuerySerializer()
    created_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%b-%Y, %H:%M:%S")
    class Meta:
        model = Notification
        fields = ("id", "query", "updated_on", "created_on")
        depth = 1
