from django.db import models
from django.urls import reverse
import uuid

# Create your models here.

class Features(models.Model): # To be removed or updated
    name = models.TextField(max_length=200, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for features"""
        return reverse('feature', args=[str(self.id)])
