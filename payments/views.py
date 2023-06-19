from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import razorpay
from booking.models import Order
from .models import *
from .serializers import *
from ultraxpert.settings import PAYMENT_TEST_API_KEY, PAYMENT_TEST_SECRET_KEY


class PaymentView(APIView):
    "Payment API"
    permission_classes = (IsAuthenticated,)
    client = razorpay.Client(auth=(PAYMENT_TEST_API_KEY, PAYMENT_TEST_SECRET_KEY))

    def get(self, request, format=None):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.get_payment_history_list,
                2: self.payment_details
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
        
    def get_payment_history_list(self):
        pass

    def payment_details(self):
        pass
        

    def post(self, request, format=None):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.create_payment
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)
        
    def create_payment(self):
        try:
            order_id = self.data.get("order_id")
            payment_method = self.data.get("payment_method")
            bank = self.data.get("bank_detail")
            order = Order.objects.get(order_id=order_id)
            response = self.client.payment.createPaymentJson({
                "amount": int(order.service.price)*100,
                "currency": order.service.currency,
                "email": order.customer.user.email,
                "contact": str(order.customer.user.mobile),
                "order_id": order.order_id,
                "method": payment_method,
                "bank": bank
                })
            obj = Payment(
                user = self.user,
                payment_id = response["razorpay_payment_id"],
                order_no = order.order_id,
                amount = order.service.price,
                currency = order.service.currency,
                payment_method = payment_method,
                payment_response = response,
                callback_url = response["next"][0]["url"]
            )
            obj.save()
            serialized_data = PaymentSerializer(obj)
            self.ctx = {"msg":"Payment Created Successfully!","data":serialized_data.data}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!","error_msg": str(e)}
            self.status = status.HTTP_400_BAD_REQUEST

        







