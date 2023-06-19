from django.contrib import admin
from .models import *

from django.contrib.admin import ModelAdmin



class ServiceAdmin(ModelAdmin):
    """Service Details On Admin"""
    list_display       = ("id", "service_name", "duration", "price")
    search_fields      = ("id", "service_name", "price")
    readonly_fields    = ("updated_on", "date_created")
    filter_horizontal  = ()
    list_filter        = ()
    fieldsets          = ()
    ordering           = ("id",)

class BankAdmin(ModelAdmin):
    """Bank Details Admin"""
    list_display       = ("id", "account_holder", "bank_name", "account_number")
    search_fields      = ("id", "account_holder", "bank_name")
    readonly_fields    = ("updated_on", "timestamp")
    filter_horizontal  = ()
    list_filter        = ()
    fieldsets          = ()
    ordering           = ("id",)


# Registration on Django Admin Panel
admin.site.register(Services, ServiceAdmin),
admin.site.register(BankDetail, BankAdmin),
admin.site.register([
    Expert,
    Skills,
    Education,
    Experience,
    Category,
    Event,
    EventSchedule,
    EventScheduleTime,
    ServiceReaction,
    ServiceViews,
    Achievements,
    Offers,
    ExpertFollowers,
    ExpertRatings
    ])
