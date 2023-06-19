from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .manager import CustomUserManager

class UserAccount(AbstractBaseUser, PermissionsMixin):
    """Model For Saving User Account Details"""
    username         = None
    first_name       = models.CharField(max_length=100, verbose_name="First Name", blank=True, null=True)
    last_name        = models.CharField(max_length=100, verbose_name="Last Name", blank=True, null=True)
    mobile           = PhoneNumberField(blank=True, null=True, unique=True)
    email            = models.EmailField(unique=True, verbose_name="Email Address", blank=True, null=True)
    dob              = models.DateField(verbose_name="Date Of Birth", blank=True, null=True)
    marital_status   = models.CharField(max_length=50, verbose_name="Marital Status", blank=True ,null=True)
    anniversary_date = models.DateField(verbose_name="Anniversary Date", blank=True, null=True)
    user_otp         = models.CharField(max_length=6, verbose_name="User OTP", blank=True, null=True)
    profile_img      = models.URLField(verbose_name="Profile Image", blank=True, null=True)
    is_staff         = models.BooleanField(default=False, verbose_name="Staff")
    is_superuser     = models.BooleanField(default=False, verbose_name="Admin")
    is_active        = models.BooleanField(default=True, verbose_name="Active")
    is_verified      = models.BooleanField(default=False, verbose_name="Verified")
    is_online        = models.BooleanField(default=True, verbose_name="Online")
    is_expert        = models.BooleanField(default=False, verbose_name="Is expert")
    gender           = models.CharField(max_length=10, verbose_name="Gender", choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")), blank=True, null=True)
    refer_code       = models.CharField(max_length=10, unique=True, verbose_name="Refer Code", blank=True, null=True)
    reffered_by      = models.CharField(max_length=10, verbose_name="Refereed By", blank=True, null=True)
    updated_on       = models.DateTimeField(auto_now=True, verbose_name="Last Update On", blank=True, null=True) 
    date_joined      = models.DateTimeField(auto_now_add=True, verbose_name="Joining Date", blank=True, null=True)
    objects          = CustomUserManager()
    USERNAME_FIELD   = 'email'
    REQUIRED_FIELDS  = []

    def __str__(self) -> str:
        return str(self.first_name) + " " + str(self.last_name)


    class Meta:
        verbose_name = 'User Account'
        verbose_name_plural = 'User Accounts'
        ordering = ("-date_joined",)



class UserEmails(models.Model):
    email = models.EmailField(verbose_name="User Email", blank=True,null=True)
    otp = models.PositiveIntegerField(null=True, blank=True, verbose_name="OTP")
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Last Update On", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Joining Date", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.email)
    class Meta:
        verbose_name = 'User Email'
        verbose_name_plural = 'User Emails'
        ordering = ("-created_on",)
