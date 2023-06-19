from django.db import models
from useraccounts.models import UserAccount


class Enterprise(models.Model):
    owner           = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="Owner", blank=True, null=True)
    registration_no = models.CharField(max_length=500, verbose_name="Company Registration Number", blank=True, null=True)
    name            = models.CharField(max_length=255, verbose_name="Name", blank=True, null=True)
    description     = models.TextField(verbose_name="Description", blank=True, null=True)
    website_link    = models.URLField(verbose_name="Website", blank=True, null=True)
    strength        = models.PositiveIntegerField(default=0, verbose_name="Strength")
    registered_on   = models.DateField(blank=True, null=True, verbose_name="Registered On")
    date_created    = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    date_updated    = models.DateTimeField(auto_now=True, verbose_name="Date Updated")
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Enterprises"
        ordering = ("-date_created",)

class Training(models.Model):
    name            = models.CharField(max_length=255, verbose_name="Course Name")
    technology      = models.CharField(max_length=255, verbose_name="Technology", blank=True, null=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price", blank=True)
    start_time      = models.TimeField(verbose_name="Start Time", blank=True, null=True)
    end_time        = models.TimeField(verbose_name="End Time", blank=True, null=True)
    start_date      = models.DateField(verbose_name="Start Date", blank=True, null=True)
    duration        = models.PositiveIntegerField(verbose_name="Training Duration in Days", default=0)
    date_created    = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    date_updated    = models.DateTimeField(auto_now=True, verbose_name="Date Updated")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Trainings"
        ordering = ("-date_created",)

class Employee(models.Model):
    user            = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="Employee")
    enterprise      = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name="Enterprise")
    role            = models.CharField(max_length=255, verbose_name="Role", blank=True, null=True)
    training        = models.ManyToManyField(Training, verbose_name="Training", blank=True)
    about_me        = models.TextField(verbose_name="About Me", blank=True, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")
    date_updated    = models.DateTimeField(auto_now=True, verbose_name="Date Updated")


    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    class Meta:
        verbose_name_plural = "Employees"
        ordering = ("-date_created",)
