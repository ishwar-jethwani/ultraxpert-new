from django.db import models
from useraccounts.models import *
from customers.models import Customer
from help_function.main import FileHandling

class Expert(models.Model):
    """Expert Details Model"""
    user            = models.OneToOneField(UserAccount, on_delete=models.CASCADE, verbose_name="Expert")
    about_me        = models.TextField(verbose_name="About Me", blank=True, null=True)
    profession      = models.CharField(max_length=30, blank=True, null=True)
    level           = models.CharField(max_length=10, blank=True, null=True)
    profile_view    = models.PositiveIntegerField(default=0, verbose_name="Profile View")
    updated_on      = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on      = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.user.first_name) + " " + str(self.user.last_name)
    
    class Meta:
        verbose_name_plural = 'Experts'
        ordering = ("-updated_on",)


class Skills(models.Model):
    """This model contains skillset of expert"""
    expert      = models.OneToOneField(Expert, on_delete=models.CASCADE, verbose_name = "Expert")
    skills_json = models.JSONField(default=list, verbose_name="Skills")
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)
    
    class Meta:
        verbose_name_plural = 'Skills'
        ordering = ("-updated_on",)

class Education(models.Model):
    """Expert Education"""
    expert      = models.OneToOneField(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    education   = models.JSONField(default=list, verbose_name="Education")
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)
    
    def __str__(self) -> str:
        return  str(self.expert.pk) + "-" + str(self.pk)
    
    class Meta:
        verbose_name_plural = 'Education'
        ordering = ("-updated_on",)


class Experience(models.Model):
    """Expert Education"""
    expert      = models.OneToOneField(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    experience  = models.JSONField(default=list, verbose_name="Experience")
    years       = models.PositiveIntegerField(default=0, verbose_name="Years Of Experience")
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on  = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)
    
    class Meta:
        verbose_name_plural = 'Experiences'
        ordering = ("-updated_on",)  


class Category(models.Model):
    """Model For Category Details"""
    name            = models.CharField(max_length=200,  blank=True,  null=True)
    img             = models.URLField(null=True, blank=True)
    number          = models.PositiveIntegerField(null=True, blank=True)
    parent_category = models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name="Parant Category", null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories" 
        ordering = ("number",)

    def __str__(self) -> str:
        return self.name



class Services(models.Model):
    """Model For Details Of Services"""
    expert       = models.ForeignKey(Expert, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100,  verbose_name="Title", blank=True, null=True)
    service_img  = models.URLField(blank=True, null=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description  = models.TextField(verbose_name="Description", blank=True, null=True)
    duration     = models.CharField(max_length=10, verbose_name="Duration", blank=True,  null=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price", blank=True)
    currency     = models.CharField(max_length=10, verbose_name="Currency", choices=(("INR", "INR"), ("USD", "USD"), ("GBP", "GBP")), default="INR", blank=True, null=True)
    tags         = models.JSONField(default=list, verbose_name="tags")
    updated_on   = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.service_name

    class Meta:
        verbose_name_plural = "Services" 
        ordering = ("-updated_on",)



class ServiceReaction(models.Model):
    """Reaction on service"""
    obj          = FileHandling("structure/emoji.json")
    user         = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    service      = models.OneToOneField(Services, on_delete=models.CASCADE)
    reactions    = models.JSONField(default=obj.get_data(), verbose_name="Reactions")
    updated_on   = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank = True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    


    def __str__(self) -> str:
        return str(self.user.pk) + str(self.pk)

    class Meta:
        verbose_name_plural = "Services Reactions" 
        ordering = ("-updated_on",)


class ServiceViews(models.Model):
    """Views on services"""
    user    = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user.pk)

    class Meta:
        verbose_name_plural = "Service Views" 


class Event(models.Model):
    """ Event For Booking """
    expert              = models.ForeignKey(Expert, on_delete=models.CASCADE)
    service             = models.ForeignKey(Services, on_delete=models.CASCADE, blank=True, null=True)
    notify_before       = models.BooleanField(default=False)
    notify_before_time  = models.CharField(max_length=50, verbose_name="Notify Before Time", blank=True, null=True)
    notify_after        = models.BooleanField(default=False)
    notify_after_time   = models.CharField(max_length=50, verbose_name="Notify After Time", blank=True, null=True)
    updated_on          = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    created_on          = models.DateTimeField(auto_now_add=True,  verbose_name="Event Created On")

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.service.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ("-created_on",)


class EventSchedule(models.Model):
    """Model For Scheduling Events"""
    day = models.CharField(verbose_name="Day", max_length=30, blank=True, null=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.event.pk) + "-" + str(self.pk)


class EventScheduleTime(models.Model):
    """Model For Event Time Details """
    schedule    = models.ForeignKey(EventSchedule,models.CASCADE)
    start_time  = models.CharField(max_length=255, verbose_name="start time", blank=True, null=True)
    end_time    = models.CharField(max_length=255, verbose_name="End time", blank=True, null=True)
    timezone    = models.CharField(max_length=255, verbose_name="timeZone", blank=True, null=True)
    duration    = models.PositiveIntegerField(default=0)
    booked      = models.BooleanField(default=False)
    disable     = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.schedule.pk) + "-" + str(self.pk)


class Achievements(models.Model):
    """Achievements"""
    expert      = models.OneToOneField(Expert, on_delete=models.CASCADE)
    achievements = models.JSONField(default=list, blank=True, null=True)
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Achievements"
        ordering = ("-updated_on",)

class Offers(models.Model):
    """Offers for Customer"""
    expert        = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Experts")
    customer      = models.ForeignKey(Customer,on_delete=models.CASCADE, verbose_name="Customer")
    offer         = models.JSONField(default=dict,verbose_name="Offer")
    updated_on    = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created  = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Offers"
        ordering = ("-updated_on",)

class ExpertFollowers(models.Model):
    """Expert Follower"""
    expert         = models.OneToOneField(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    customer       = models.ManyToManyField(Customer, verbose_name="Follower")
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    timestamp      = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Followers"
        ordering = ("-updated_on",)

class ExpertRatings(models.Model):
    "Expert Ratings"
    expert      = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    customer    = models.ForeignKey(Customer,on_delete=models.CASCADE, verbose_name="Customers")
    ratings     = models.PositiveIntegerField(default=0,verbose_name="Ratings")
    review      = models.CharField(max_length=500,verbose_name="Review")  
    updated_on  = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    timestamp   = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Ratings"
        ordering = ("-timestamp",)


class BankDetail(models.Model):
    """Model For Saving Bank Details"""
    expert         = models.OneToOneField(Expert, on_delete=models.CASCADE)
    account_holder = models.CharField(max_length=100, verbose_name="Account Holder Name", blank=True, null=True)
    bank_name      = models.CharField(max_length=1000, verbose_name="Bank Name", blank=True, null=True)
    account_number = models.CharField(max_length=20, verbose_name="Account_number", blank=True, null=True)
    ifsc_code      = models.CharField(max_length=100, verbose_name="IFSC Code", blank=True, null=True)
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    timestamp      = models.DateTimeField(auto_now_add=True, verbose_name="Created On", blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Bank Details"
        ordering = ("-updated_on",)
