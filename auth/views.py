from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from core.utils import report_log
 

class LoginView(APIView):
    """
    View responsável pela autenticação de usuários via JWT.

    Endpoint:
        POST /api/auth/login/
    """    
    def post(self, request: Request) -> Response:
        """
        Autentica o usuário e retorna tokens JWT.

        Body esperado (JSON):
            - username
            - password
        """
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if not user:
            report_log(
                user=None,
                action="Login",
                status="ERROR",
                message="Credenciais inválidas"
            )
            return Response(
                {"detail": "Credenciais inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        refresh = RefreshToken.for_user(user)
        
        report_log(
            user=user,
            action="Login",
            status="SUCCESS",
            message="Login realizado com sucesso"
        )
        
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )
        
class RefreshTokenView(APIView):
    """
    View responsável por renovar o access token a partir do refresh token.

    Endpoint:
        POST /api/auth/refresh/
    """
    def post(self, request: Request) -> Response:
        refresh_token = request.data.get("refresh")
        
        try:
            refresh = RefreshToken(refresh_token)
            
            return Response(
                {
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
           )
        except Exception:
            return Response(
                {"detail": "Refresh token inválido"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
class LogoutView(APIView):
    """
    View responsável por realizar logout do usuário.

    Endpoint:
        POST /api/auth/logout/
    """
    def post(self, request: Request) -> Response:
        refresh_token = request.data.get("refresh")
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Logout",
                status="SUCCESS",
                message="Logout realizado com sucesso"
            )
            return Response(
                {"detail": "Logout realizado com sucesso"},
                status=status.HTTP_200_OK    
            )
        
        except Exception:
            return Response(
                {"detail": "Token inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
            