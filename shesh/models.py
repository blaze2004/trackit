# import environ
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

# env = environ.Env()
# environ.Env.read_env()

# Create your models here.
class AttendanceReport(models.Model):
    """This model contains attendance report data of the meetings."""

    meetCode = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    startTime = models.TimeField(null=False, blank=False)
    stopTime = models.TimeField(null=False, blank=False)
    attendanceData = models.JSONField(null=False, blank=False)
    slug = models.CharField(max_length=255,null=False, unique=True, blank=True)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared = models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.meetCode

    def get_absolute_url(self):
        """Returns the url to access a detail record for Attendance."""
        return reverse('attendance-report', args=[self.meetCode, str(self.id)])

@receiver(pre_save, sender=AttendanceReport)
def create_slug(sender, instance, *args, **kwargs):

    if instance.slug == '':

        if AttendanceReport.objects.count()>0:
            uuid  = AttendanceReport.objects.all().last().pk
            instance.slug = instance.meetCode +"-"+ str(uuid)
        else:
            instance.slug = instance.meetCode

# @receiver(pre_save, sender=User)
# def create_contact(sender, instance, *args, **kwargs):
#     hapikey = env("HAPI_KEY")
#     endpoint = 'https://api.hubapi.com/contacts/v1/contact/'
#     headers = {}
#     headers["Content-Type"]="application/json"
#     headers["authorization"] = f"Bearer {hapikey}"

#     data = json.dumps({
#             "properties": [
#             {
#               "property": "email",
#               "value": instance.email
#             },
#             {
#               "property": "firstname",
#               "value": instance.first_name
#             },
#             {
#               "property": "lastname",
#               "value": instance.last_name
#             }
#         ]
#     })

#     r = requests.post(url = endpoint, data = data, headers = headers )
