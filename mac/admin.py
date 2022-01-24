from django.contrib import admin
from django.db.models.base import Model

# Register your models here.
from .models import Class,Student,Attendance_Record

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Attendance_Record)