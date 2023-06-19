from django.db import models
from experts.models import Expert

class Questions(models.Model):
    """Question for expert test"""
    question     = models.TextField(max_length=5000, verbose_name="Question", blank=True, null=True)
    options      = models.JSONField(default=dict, blank=True, null=True)
    answer       = models.CharField(max_length=100000, verbose_name="Answer", blank=True, null=True)
    topic        = models.CharField(max_length=200, verbose_name="Topic", blank=True, null=True)
    seq_num      = models.PositiveIntegerField(default=0, verbose_name="Sequence Number")
    updated_on   = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self) -> str:
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ("-seq_num",)   

class ExpertTestReport(models.Model):
    """Test Details For Expert"""
    expert         = models.OneToOneField(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    qualified      = models.BooleanField(default=False, verbose_name="Qualified")
    correct_ans    = models.PositiveIntegerField(default=0, verbose_name="Correct Answers")
    test_scheduled = models.DateTimeField(blank=True, null=True, verbose_name="Test Scheduled Date")
    start_time     = models.TimeField(blank=True, null=True, verbose_name="Test Start Time")
    end_time       = models.TimeField(blank=True, null=True, verbose_name="Test Start Time")
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Expert Report"
        ordering = ("-updated_on",)   

class InterviewSchedule(models.Model):
    """Expert Interviews"""
    expert         = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    meeting_link   = models.URLField(blank=True, null=True, verbose_name="Meeting Link")
    start_time     = models.TimeField(blank=True, null=True, verbose_name="Test Start Time")
    end_time       = models.TimeField(blank=True, null=True, verbose_name="Test Start Time")
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    
    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Interviews"
        ordering = ("-updated_on",)   

class ExpertAnswers(models.Model):
    """Answers for expert test"""
    expert         = models.ForeignKey(Expert, on_delete=models.CASCADE, verbose_name="Expert")
    question       = models.ForeignKey(Questions, on_delete=models.CASCADE, verbose_name="Question")
    answer         = models.CharField(max_length=100000, verbose_name="Answer", blank=True, null=True)
    updated_on     = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank=True, null=True)
    date_created   = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.expert.pk) + "-" + str(self.pk)

    class Meta:
        verbose_name_plural = "Expert Answers"
        ordering = ("-updated_on",)
