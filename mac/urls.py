from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('save/', views.save, name='save'),
    path('save-attendance/', views.save_to_database, name='save_attendance'),
    path('report-view/', views.report_view, name='report_view'),
    path('docs/', views.docs, name='docs'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('delete-record/', views.delete_record, name='delete_record'),
]