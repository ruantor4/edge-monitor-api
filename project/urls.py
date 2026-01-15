
"""
Arquivo central de roteamento da aplicação.
Este módulo define:
- Rotas administrativas
- Exposição do schema OpenAPI
- Interface Swagger
- Inclusão das rotas dos módulos da aplicação
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from project import settings

urlpatterns = [
    
    # ADMIN
    # GET /admin/
    path('admin/', admin.site.urls),
    
    # SCHEMA OPENAPI
    # GET /api/schema/
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    
    # SWAGGER UI
    # GET /
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    
    # USUÁRIOS
    # GET    /api/user/
    # POST   /api/user/
    # GET    /api/user/{id}/
    # PUT    /api/user/{id}/
    # DELETE /api/user/{id}/
    path("api/", include("users.urls")),
    
    # AUTENTICAÇÃO
    # POST /api/authentication/login/
    # POST /api/authentication/renovate/
    # POST /api/authentication/logout/
    path("api/authentication/", include("auth.urls")),
    
    # MONITORAMENTO
    # POST /api/monitoring/
    path("api/monitoring/", include("monitoring.urls")),
    
    # DASHBOARD
    # GET /api/dashboard/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
    path("api/dashboard/", include("dashboard.urls"))

]

# ARQUIVOS DE MÍDIA (AMBIENTE DE DESENVOLVIMENTO)
# Exposição de arquivos enviados
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)
