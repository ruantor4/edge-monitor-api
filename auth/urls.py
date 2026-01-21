"""
    Rotas responsáveis pela autenticação e gerenciamento de tokens JWT.

    Este módulo define exclusivamente os endpoints de autenticação,
    delegando toda a lógica de negócio para as respectivas views.
"""
from django.urls import path

from auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetRequestView, RenovateTokenView


urlpatterns = [
    
    # AUTENTICAÇÃO (JWT)
    
    # POST /api/authentication/login/
    path("login/", LoginView.as_view(), name="login"),
    
    
    # RENOVAÇÃO DE TOKEN
    
    # POST /api/authentication/renovate/
    path("renovate/", RenovateTokenView.as_view(), name="token-renovate"),
    
    
    # LOGOUT
    
    # POST /api/authentication/logout/
    path("logout/", LogoutView.as_view(), name="logout"),
    
    
    # RECUPERAÇÃO DE SENHA
    
    # POST /api/authentication/password-reset/
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),

    # POST /api/authentication/password-reset/confirm/
    path(
        "password-reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]