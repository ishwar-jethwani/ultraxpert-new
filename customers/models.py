from django.db import models
from useraccounts.models import *

class Customer(models.Model):
    """Customers Details Model"""
    user       = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    about_me   = models.TextField(verbose_name="About Me", blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.user.first_name) + " " + str(self.user.last_name)
    
    class Meta:
        verbose_name_plural = 'Customers'
        ordering = ("-updated_on",)

class CustomerInterest(models.Model):
    "Customer Interest Details"
    customer      = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    interest_list = models.JSONField(default=list, verbose_name="Interest Fields", blank=True, null=True)
    updated_on    = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created  = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.customer.pk)
    
    class Meta:
        verbose_name_plural = "Customer Interests" 
        ordering = ("-updated_on",)

class FavoriteExpert(models.Model):
    customer       = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    experts        = models.ManyToManyField(to="experts.Expert", verbose_name="Experts", null=True, blank=True)
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.customer.pk)
    
    class Meta:
        verbose_name_plural = "Favorite Experts" 
        ordering = ("-updated_on",)


class CustomerQuery(models.Model):
    """Customer Query Details"""
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    subject         = models.CharField(max_length=200, verbose_name="Subject", blank=True, null=True)
    technology_name = models.CharField(max_length=50, verbose_name="Technology Name", blank=True, null=True)
    topic           = models.CharField(max_length=50,verbose_name="Topic", blank=True, null=True)
    description     = models.TextField(verbose_name="Description", blank=True, null=True)
    medium          = models.CharField(max_length=50, verbose_name="Medium", blank=True, null=True)
    status          = models.CharField(max_length=20,verbose_name="Status", blank=True, null=True)
    updated_on      = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.customer.pk) + "-" + str(self.pk)
    
    class Meta:
        verbose_name_plural = "Customers Queries" 
        ordering = ("-updated_on",)

class RecentlyViewedExpert(models.Model):
    customer       = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Customer")
    experts        = models.ManyToManyField(to="experts.Expert", verbose_name="Experts", null=True, blank=True)
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.customer.pk)
    
    class Meta:
        verbose_name_plural = "Recently Viewed Experts" 
        ordering = ("-updated_on",)