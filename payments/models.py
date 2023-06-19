from django.db import models
from useraccounts.models import UserAccount


class Payment(models.Model):
    """Model For Payment"""
    user              = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    amount            = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_id        = models.CharField(max_length=255, blank=True, null=True, verbose_name="PaymentID")
    order_no          = models.CharField(max_length=20,verbose_name="order_no",blank=True,null=True)
    payment_status    = models.CharField(max_length=255, blank=True, null=True, verbose_name="PaymentStatus")
    payment_method    = models.CharField(max_length=255, blank=True, null=True, verbose_name="PaymentResponse")
    payment_response  = models.JSONField(blank=True, null=True)
    callback_url      = models.URLField(verbose_name="Callback URL", blank=True, null=True)
    currency          = models.CharField(max_length=30, verbose_name="Currency", blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    class Meta:
        db_table = 'payments'
        verbose_name_plural = "Payments" 
        ordering = ("-created_at",)


class Refund(models.Model):
    """Model For Refund Status"""
    user            = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    refund_id       = models.CharField(max_length=500,verbose_name="Refund ID",blank=True,null=True)
    order_no        = models.CharField(max_length=20,verbose_name="order_no",blank=True,null=True)
    response        = models.JSONField(verbose_name="Refund Response",blank=True,null=True)
    currency        = models.CharField(max_length=30, verbose_name="Currency", blank=True, null=True)
    refund_status   = models.CharField(max_length=30, verbose_name="RefundStatus", blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    

    def __str__(self) -> str:
        return self.refund_id

    class Meta:
        ordering = ("-created_at",)



