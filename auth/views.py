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