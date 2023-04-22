from django.contrib import admin
from .models import AttendanceReport

@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ("meetCode", "date", "userId")
    search_fields = ("meetCode",)
    list_filter = ("userId",)