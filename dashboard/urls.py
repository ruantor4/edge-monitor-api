from django.urls import path

from dashboard.views import DashboardView



urlpatterns = [
    
    # DASHBOARD
    # GET /api/dashboard/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    path("", DashboardView.as_view(), name="dashboard")        
]