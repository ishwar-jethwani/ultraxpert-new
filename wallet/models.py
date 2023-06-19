from django.db import models
import uuid
from useraccounts.models import UserAccount

class Wallet(models.Model):
    """User Credit Store"""
    wallet_id  = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False) 
    user       = models.OneToOneField(UserAccount, on_delete=models.CASCADE, verbose_name="User")
    balance    = models.DecimalField(default=0, max_digits=10, decimal_places=3, verbose_name="Balance")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.wallet_id)
    class Meta:
        ordering = ("-created_on",)
        verbose_name_plural = "Wallets"

class Transaction(models.Model):
    "Transaction Details"
    wallet  = models.ForeignKey(Wallet, on_delete=models.CASCADE, verbose_name="Wallet")
    transaction_balance = models.DecimalField(default=0, max_digits=10, decimal_places=3, verbose_name="Credit")
    credit = models.BooleanField(default=False, verbose_name="Credit")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.wallet.wallet_id)
    class Meta:
        ordering = ("-created_on",)
        verbose_name_plural = "Transactions"
