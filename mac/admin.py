from django.contrib import admin
from django.db.models.base import Model

# Register your models here.
from .models import Features

admin.site.register(Features)