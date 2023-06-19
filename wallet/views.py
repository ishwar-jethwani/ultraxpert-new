from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import *
from datetime import datetime
from decimal import Decimal

class WalletView(APIView):
    """User Credit Details"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        self.data = request.GET
        self.user = request.user
        if "action" in self.data:
            action = int(self.data.get("action"))
            action_mapper = {
                1: self.get_balance,
                2: self.get_history
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def get_balance(self):
        try:
            wallet = Wallet.objects.get(user=self.user)
            last_update_on = wallet.updated_on.strftime("%d-%b-%Y, %H:%M:%S")
            registered_on = wallet.created_on.strftime("%d-%b-%Y, %H:%M:%S")
            data_dict = {
                "wallet_id": wallet.wallet_id,
                "balance": wallet.balance,
                "last_updated": last_update_on,
                "registered_on": registered_on
            }
            self.ctx = {"msg": "Your Wallet Details Loaded!", "data": data_dict}
            self.status = status.HTTP_200_OK
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR           
        
    def get_history(self):
        start_date = self.data.get("start_date")
        end_date = self.data.get("end_date")
        try:
            wallet = Wallet.objects.get(user=self.user)
            transactions = Transaction.objects.filter(wallet=wallet)
            if transactions.exists():
                if start_date and end_date:
                    start_date = datetime.strptime(start_date,"%d/%m/%Y")
                    end_date = datetime.strptime(end_date,"%d/%m/%Y")
                    transactions.filter(created_on__range=(start_date, end_date))
                serialized_data = TransactionSerializer(transactions, many=True)
                self.ctx = {"msg": "History Loaded Successfully!", "data": serialized_data.data}
                self.status = status.HTTP_200_OK
            else:
                self.ctx = {"msg": "No Data Found!", "data": []}
                self.status = status.HTTP_404_NOT_FOUND
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e)}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    def post(self, request):
        self.data = request.data
        self.user = request.user
        if "action" in self.data:
            action = self.data.get("action",1)
            action_mapper = {
                1: self.add_wallet,
                2: self.add_balance,
                3: self.transactions
            }
            action_status = action_mapper.get(action, lambda: "Invalid")()
            if action_status == "Invalid":
                self.ctx = {"msg": "Choose Wrong Option !", "data": None}
                self.status = status.HTTP_400_BAD_REQUEST
            return Response(self.ctx, self.status)
        else:
            return Response({"msg": "Action is not in dict", "data": None}, status.HTTP_400_BAD_REQUEST)

    def add_wallet(self):
        try:
            obj = Wallet(user=self.user)
            obj.save()
            last_update_on = obj.updated_on.strftime("%d-%b-%Y, %H:%M:%S")
            registered_on = obj.created_on.strftime("%d-%b-%Y, %H:%M:%S")
            data_dict = {
                "wallet_id": obj.wallet_id,
                "balance": obj.balance,
                "last_updated": last_update_on,
                "registered_on": registered_on
            }
            self.ctx = {"msg":"Wallet Created Successfully!", "data": data_dict}
            self.status = status.HTTP_201_CREATED
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def add_balance(self):
        balance = self.data.get("balance")
        try:
            obj = Wallet.objects.get(user=self.user)
            obj.balance += balance
            obj.save(update_fields=["balance"])
            last_update_on = obj.updated_on.strftime("%d-%b-%Y, %H:%M:%S")
            registered_on = obj.created_on.strftime("%d-%b-%Y, %H:%M:%S")
            transaction_obj = Transaction(wallet=obj, transaction_balance=balance, credit=True)
            transaction_obj.save()
            data_dict = {
                "wallet_id": obj.wallet_id,
                "balance": obj.balance,
                "last_updated": last_update_on,
                "registered_on": registered_on
            }
            self.ctx = {"msg":"Credit Added Successfully!", "data": data_dict}
            self.status = status.HTTP_200_OK 
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR

    def transactions(self):
        charge = self.data.get("charge")
        try: 
            obj = Wallet.objects.get(user=self.user)
            if obj.balance >= Decimal(charge) if charge else 0:
                obj.balance -= Decimal(charge)
                obj.save(update_fields=["balance"])
                last_update_on = obj.updated_on.strftime("%d-%b-%Y, %H:%M:%S")
                registered_on = obj.created_on.strftime("%d-%b-%Y, %H:%M:%S")
                transaction_obj = Transaction(wallet=obj, transaction_balance=charge)
                transaction_obj.save()
                transaction_date = transaction_obj.created_on.strftime("%d-%b-%Y, %H:%M:%S")
                data_dict = {
                    "wallet_id": obj.wallet_id,
                    "balance": obj.balance,
                    "last_transaction": transaction_obj.transaction_balance,
                    "credit": transaction_obj.credit,
                    "transaction_date":transaction_date,
                    "last_updated": last_update_on,
                    "registered_on": registered_on
                }
                self.ctx = {"msg":"Credit Added Successfully!", "data": data_dict}
                self.status = status.HTTP_200_OK 
            else:
                self.ctx = {"msg":"Insufficient Credit"}
                self.status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            self.ctx = {"msg": "Something went wrong!", "error_msg":str(e), "data": None}
            self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
