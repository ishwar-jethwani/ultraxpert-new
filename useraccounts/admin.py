from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    """Expert Account Admin"""
    list_display       = ("id", "first_name", "last_name", "mobile", "email", "is_verified", "is_staff", "is_superuser", "is_active", "refer_code", "reffered_by")
    search_fields      = ("id", "email", "refer_code")
    ordering           = ("id",)
    readonly_fields    = ("date_joined", "updated_on")
    add_fieldsets = (
    (None, {
        "classes": ("wide",),
        "fields": ("email", "mobile", "first_name", "last_name", "password1", "password2"),
    }),
    )
    fieldsets = (
    (None, {
        "classes": ("wide",),
        "fields": ("first_name", "last_name", "mobile", "email", "user_otp", "is_verified", "is_staff", "is_superuser", "is_active", "refer_code", "reffered_by"),
    }),
    )



admin.site.register(UserAccount,AccountAdmin)
admin.site.register(UserEmails)
