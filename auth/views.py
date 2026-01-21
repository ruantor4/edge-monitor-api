from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from project import settings

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RenovateTokenSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

from core.utils import report_log

token_generator = PasswordResetTokenGenerator()
 
class LoginView(APIView):
    """
    View responsável pela autenticação de usuários utilizando JWT.

    Esta view recebe credenciais válidas e retorna um par de tokens
    (access e renovate), delegando a autenticação ao backend do Django.
    """  
    
    permission_classes = [AllowAny]
    
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

class RenovateTokenView(APIView):
    """
    View responsável por gerar um novo access token a partir
    de um renovate token válido.
    """
    permission_classes = [AllowAny]
    
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


class LogoutView(APIView):
    """
    View responsável por realizar o logout do usuário.

    Executa a invalidação do renovate token informado,
    impedindo novas renovações de access token.
    """
    
    permission_classes = [IsAuthenticated]
    
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
            
class PasswordResetRequestView(APIView):
    """
    View responsável por iniciar o processo de recuperação de senha.

    IMPORTANTE:
    - Nunca informa se o e-mail existe ou não
    - Evita enumeração de usuários
    """
    
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
            }
        },
    )
    def post(self, request: Request) -> Response:
        """
        Processa a solicitação de recuperação de senha.

        Responsabilidades:
        - Validar o e-mail informado
        - Gerar token seguro de redefinição
        - Enviar e-mail com link de recuperação
        - NÃO revelar se o e-mail existe ou não
        """ 
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            
            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password-confirm.html"
                f"?uid={uid}&token={token}"
            )

            send_mail(
                subject="Recuperação de senha",
                message=f"Use o link para redefinir sua senha:\n{reset_link}",
                from_email=None,
                recipient_list=[email],
                fail_silently=True,
            )

            report_log(
                user=user,
                action="Password Reset Request",
                status="INFO",
                message="Solicitação de recuperação de senha enviada"
            )

        return Response(
            {"detail": "Se o e-mail existir, um link será enviado"},
            status=status.HTTP_200_OK
        )
        
        
class PasswordResetConfirmView(APIView):
    """
    View responsável por confirmar a redefinição de senha do usuário.
    """        
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"},
                },
            }
        },
    )
    def post(self, request: Request) -> Response:
        """
        Processa a redefinição de senha.

        Responsabilidades:
        - Validar token e UID
        - Atualizar senha do usuário
        - Invalidar token após uso
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(
                urlsafe_base64_decode(serializer.validated_data["uid"])
            )
            user = User.objects.get(pk=uid)

            if not token_generator.check_token(
                user, serializer.validated_data["token"]
            ):
                raise ValueError("Token inválido")

            user.set_password(serializer.validated_data["password"])
            user.save()

            report_log(
                user=user,
                action="Password Reset Confirm",
                status="SUCCESS",
                message="Senha redefinida com sucesso"
            )

            return Response(
                {"detail": "Senha redefinida com sucesso"},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"detail": "Token inválido ou expirado"},
                status=status.HTTP_400_BAD_REQUEST
            )