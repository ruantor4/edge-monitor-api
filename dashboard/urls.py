"""
Rotas responsáveis pela exposição de dados consolidados
para consumo do dashboard.
Este módulo define exclusivamente os endpoints relacionados
à visualização e consulta de eventos de monitoramento,
delegando toda a lógica de agregação e filtragem para a view.
"""
from django.urls import path
from dashboard.views import DashboardView

urlpatterns = [
    
    # DASHBOARD
    # GET /api/dashboard/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    path("", DashboardView.as_view(), name="dashboard")        
]