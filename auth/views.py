from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RenovateTokenSerializer
)

from core.utils import report_log
 
@extend_schema(
    request=LoginSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
                "renovate": {"type": "string"},
            },
        }
    },
)
class LoginView(APIView):
    """
    View responsável pela autenticação de usuários utilizando JWT.

    Esta view recebe credenciais válidas e retorna um par de tokens
    (access e renovate), delegando a autenticação ao backend do Django.
    """  
    
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        """
        Processa a autenticação do usuário.

        Responsabilidades:
        - Validar credenciais informadas
        - Gerar tokens JWT em caso de sucesso
        - Registrar logs de sucesso ou falha

        Espera no corpo da requisição:
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
            
        renovate = RefreshToken.for_user(user)
        
        report_log(
            user=user,
            action="Login",
            status="SUCCESS",
            message="Login realizado com sucesso"
        )
        
        return Response(
            {
                "access": str(renovate.access_token),
                "renovate": str(renovate),
                "id": user.id,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            },
            status=status.HTTP_200_OK
        )

@extend_schema(
    request=RenovateTokenSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "access": {"type": "string"},
            },
        }
    },
)         
class RenovateTokenView(APIView):
    """
    View responsável por gerar um novo access token a partir
    de um renovate token válido.
    """
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        """
        Realiza a renovação do access token.

        Responsabilidades:
        - Validar o renovate token recebido
        - Gerar um novo access token
        """
        renovate_token = request.data.get("renovate")
        
        try:
            renovate = RefreshToken(renovate_token)
            
            return Response(
                {
                    "access": str(renovate.access_token)
                },
                status=status.HTTP_200_OK
           )
        except Exception:
            return Response(
                {"detail": "renovate token inválido"},
                status=status.HTTP_401_UNAUTHORIZED
            )

@extend_schema(
    request=LogoutSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"},
            },
        }
    },
)            
class LogoutView(APIView):
    """
    View responsável por realizar o logout do usuário.

    Executa a invalidação do renovate token informado,
    impedindo novas renovações de access token.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request) -> Response:
        """
        Processa o logout do usuário.

        Responsabilidades:
        - Invalidar o renovate token recebido
        - Registrar o evento de logout em log
        """
        renovate_token = request.data.get("renovate")
        
        try:
            token = RefreshToken(renovate_token)
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
            