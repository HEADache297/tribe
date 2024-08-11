from django.db import models
from django.utils import timezone
from subject.models import Subject

# Create your models here.


class Schedule(models.Model):
    """
    The `Schedule` model represents a schedule for a subject. It contains details such as the title,
    description, associated subject, date and time, duration, and a URL link.
    """
    title = models.CharField(max_length=255, null=False, default='title')
    description = models.CharField(max_length=512, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedule')
    datetime = models.DateField(null=False, blank=False, default=timezone.now)
    duration = models.IntegerField(null=False, blank=False, default=0)
    url = models.TextField(null=False, blank=False, default='/link')

    def __str__(self):
        """
        Returns a string representation of the schedule, displaying the date/time and subject.
        """
        return f"{self.datetime} {self.subject}"