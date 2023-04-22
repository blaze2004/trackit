from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Class(models.Model):
    """This model contains classes created by users linked to their account."""

    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=500,null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for Classes."""
        return reverse('class', args=[str(self.id)])

class Student(models.Model):
    """This model contains info of students added by users in different classes."""
    name = models.CharField(max_length=50, null=False)
    class_id = models.ForeignKey(Class,on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for Students."""
        return reverse('student', args=[str(self.id)])

class Attendance_Record(models.Model):
    """This model contains attendance details every meet."""
    meet_code = models.CharField(max_length=20, null=False)
    start_time = models.TimeField(null=False)
    stop_time = models.TimeField(null=False)
    date = models.DateField(null=False)
    slug = models.CharField(max_length=255, null=False, unique=True)
    student_names = models.JSONField(null=False)
    join_time = models.JSONField(null=False)
    attended_duration = models.JSONField(null=False)
    shared = models.BooleanField(default=False, null=False, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.meet_code

    def get_absolute_url(self):
        """Returns the url to access a detail record for Students."""
        return reverse('attendance_record', args=[str(self.id)])