from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from customers.models import Customer
from experts.models import Expert,Services,EventScheduleTime
from .models import Order
import razorpay
from ultraxpert.settings import PAYMENT_TEST_API_KEY, PAYMENT_TEST_SECRET_KEY


class BookingView(APIView):
    """Booking View"""
    permission_classes = [permissions.IsAuthenticated]
    client = razorpay.Client(auth=(PAYMENT_TEST_API_KEY, PAYMENT_TEST_SECRET_KEY))
    def post(self,request):
        self.user = request.user
        self.data = request.data
        if "action" in self.data:
            action = int(self.data["action"])
            action_mapper = {
                1: self.book_service,
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST) 

    def book_service(self):
        try:
            expert_id = self.data.get("expert_id")
            service_id = self.data.get("service_id")
            slot_id = self.data.get("slot_id")
            expert = Expert.objects.get(id=expert_id)
            customer = Customer.objects.get(user=self.user)
            service = Services.objects.get(id=service_id)
            time_slot = EventScheduleTime.objects.get(id=slot_id)
            obj = Order(
                expert = expert,
                customer = customer,
                service = service,
                time_slot = time_slot
                )
            obj.save()
            response = self.client.order.create(
                {
                    "amount": int(obj.service.price)*100,
                    "currency": obj.service.currency,
                    "receipt": obj.service.service_name + " - " + obj.time_slot.start_time + " to " + obj.time_slot.end_time,
                    "partial_payment":False,
                    "payment_capture":True,
                }
            )
            obj.order_id = response.get("id")
            obj.save(update_fields=["order_id"])
            serialized_data = {
                "order_id": obj.order_id,
                "service_name": obj.service.service_name,
                "service_price": float(obj.service.price),
                "service_currency": obj.service.currency,
                "expert_name": obj.expert.user.first_name,
                "customer": obj.customer.user.first_name,
                "time_slot": obj.time_slot.start_time,
                "created_on": obj.created_on,
                "updated_on": obj.updated_on,
            }
            self.ctx = {"msg": "Service Booking Updated Successfully!", "data": serialized_data}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!","error_msg": str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
   