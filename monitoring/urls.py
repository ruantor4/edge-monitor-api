"""
Rotas responsáveis pelo recebimento de eventos de monitoramento
enviados pelos dispositivos edge.
Este módulo define exclusivamente os endpoints relacionados
ao registro de eventos de detecção, delegando toda a lógica
de validação e persistência para a view correspondente.
"""
from django.urls import path
from monitoring.views import MonitoringCreateView

urlpatterns = [
    
    # REGISTRO DE EVENTOS DE MONITORAMENTO
    # POST /api/monitoring/
    path("", MonitoringCreateView.as_view(), name="monitoring-create")        
]