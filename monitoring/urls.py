from django.urls import path

from monitoring.views import MonitoringCreateView



urlpatterns = [
    
    # REGISTRO DE EVENTOS DE MONITORAMENTO
    # POST /api/monitoring/
    path("", MonitoringCreateView.as_view(), name="monitoring-create")        
]