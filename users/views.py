from django.contrib.auth.models import User

from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from core.utils import report_log
from .serializers import UserSerializer, UserCreateSerializer


class UserListView(APIView):
    """
    View responsável por listar todos os usuários cadastrados no sistema.

    Endpoint:
        GET /api/user/
    """
    
    def get(self, request: Request) -> Response:
        """
        Retorna a lista de usuários cadastrados.

        Returns:
            Response:
                - 200: Lista de usuários (pode estar vazia)
                - 500: Erro interno inesperado
        """
        try:
            users = User.objects.all().order_by("id")
            serializer = UserSerializer(users, many=True)
        
        
            return Response(
                serializer.data, 
                status = status.HTTP_200_OK
            )

        except Exception as e:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Listar Usuários",
                status="ERROR",
                message=f"Erro inesperado ao listar usuários: {str(e)}"
            )
            return Response(
                {"detail": "Erro interno do servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserCreateView(APIView):
    """
    View responsável pela criação de usuários via API REST.

    Endpoint:
        POST /api/user/create/

    Entrada:
        JSON contendo username, email e password.

    Saída:
        Dados do usuário criado (sem senha).
    """
    def post(self, request: Request) -> Response:
        """
        Cria um novo usuário no sistema.

        Args:
            request (Request): Requisição HTTP contendo os dados do usuário.

        Returns:
            Response: Usuário criado ou mensagem de erro.
        """
        try:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = serializer.save()
            
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            report_log(
                user=None,
                action="Criar Usuário",
                status="WARNING",
                message=str(e)
            )
            return Response(
                e.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except IntegrityError as e:
            report_log(
                user=None,
                action="Criar Usuário",
                status="ERROR",
                message="Violação de integridade no banco"
            )
            return Response(
                {"detail": "Dados inválidos ou duplicados"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {"detail": "Erro interno do servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )