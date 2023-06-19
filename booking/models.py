from django.db import models
from customers.models import Customer
from experts.models import Expert, Services,EventScheduleTime


class Order(models.Model):
    """ Models For Saving Orders Details """
    order_id   = models.CharField(max_length=500, verbose_name="OrderID", blank=True, null=True)
    expert     = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    customer   = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    service    = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Services")
    time_slot  = models.ForeignKey(EventScheduleTime, on_delete=models.CASCADE, verbose_name="Time Slot")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Order On")

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.customer.pk) + "-" + str(self.service.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ("-created_on",)
