from django.db import models
from experts.models import Expert
from customers.models import Customer, CustomerQuery

class Message(models.Model):
    """Message Details"""
    sent_message = models.TextField(verbose_name="Message", null=True, blank=True)
    received_message = models.TextField(verbose_name="Message", null=True, blank=True)
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        ordering = ("-created_on",)
        verbose_name_plural = "Messages"

class Chat(models.Model):
    """Chat Details"""
    expert      = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    messages    = models.ManyToManyField(Message, verbose_name="Messages")
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.user.first_name) + " " + str(self.expert.user.last_name)

    class Meta:
        ordering = ("-created_on",)
        verbose_name_plural = "Chats"

class Notification(models.Model):
    """Notification Details"""
    query           = models.ForeignKey(CustomerQuery, verbose_name="Query", on_delete=models.CASCADE)
    accepted        = models.BooleanField(default=False, verbose_name="Accepted")
    accepted_by     = models.ForeignKey(Expert, verbose_name="Expert", on_delete=models.SET_NULL, null=True)
    updated_on      = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on      = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        ordering = ("-created_on",)
        verbose_name_plural = "Notifications"