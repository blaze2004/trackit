from django.views.generic import RedirectView
from django.urls import path

from . import views

urlpatterns = [
    path("save-attendance-report/", views.saveAttendanceReport, name="saveAttendanceReport"),
    path("delete-attendance-report/<slug>/", views.deleteAttendanceReport,name="deleteAttendanceReport"),
    path("share-attendance-report/<slug>/", views.shareAttendanceReport,name="shareAttendanceReport"),
    path("view-attendance-report/<slug>/", views.viewAttendanceReport,name="viewAttendanceReport"),
    path('', RedirectView.as_view(url="mac/", permanent=True), name='home'),
]
