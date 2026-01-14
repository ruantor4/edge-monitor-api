from django.urls import path

from monitoring.views import MonitoringCreateView



urlpatterns = [
    path("", MonitoringCreateView.as_view(), name="monitoring-create")        
]