from django.urls import path

from auth.views import LoginView, LogoutView, RenovateTokenView


urlpatterns = [
    
    # AUTENTICAÇÃO (JWT)
    # POST /api/authentication/login/
    path("login/", LoginView.as_view(), name="login"),
    
    # RENOVAÇÃO DE TOKEN
    # POST /api/authentication/renovate/
    path("renovate/", RenovateTokenView.as_view(), name="token-renovate"),
    
    # LOGOUT
    # POST /api/authentication/logout/
    path("logout/", LogoutView.as_view(), name="logout")
]