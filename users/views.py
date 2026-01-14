from django.contrib.auth.models import User

from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.utils import report_log
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserListView(APIView):
    """
    View responsável por listar todos os usuários cadastrados no sistema.

    Endpoint:
        GET /api/user/
    """
    permission_classes = [IsAuthenticated]
    
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
            
            report_log(
                    user=request.user if request.user.is_authenticated else None,
                    action="Listar Usuários",
                    status="INFO",
                    message=f"{users.count()} usuários retornados"
            )
            return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
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
    
    Criação de usuário NÃO exige autenticação.
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
            
            report_log(
                user=user,
                action="Criar Usuário",
                status="SUCCESS",
                message="Usuário criado com sucesso via API"
            )
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

class UserDetailView(APIView):
    """
    View responsável por retornar os dados de um usuário específico.

    Endpoint:
        GET /api/user/{id}/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request, pk: int) -> Response:
        """
        Retorna os dados do usuário identificado pelo ID informado.

        Args:
            request (Request): Requisição HTTP.
            pk (int): Identificador do usuário.

        Returns:
            Response:
                - 200 OK: Dados do usuário
                - 404 Not Found: Usuário não encontrado
        """
        try:
            user = get_object_or_404(User, pk=pk)
            
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Consultar Usuário",
                status="INFO",
                message=f"Usuário {pk} consultado com sucesso"
            )
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Consultar Usuário",
                status="ERROR",
                message=f"Erro ao consultar usuário {pk}: {str(e)}"
            )
            return Response(
                {"detail": "Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
   
class UserUpdateView(APIView):
    """
    View responsável por atualizar os dados de um usuário existente.

    Endpoint:
        PUT /api/user/{id}/update/
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request: Request, pk:int) -> Response:
        """
        Atualiza os dados do usuário identificado pelo ID informado.

        Args:
            request (Request): Requisição HTTP contendo os novos dados.
            pk (int): Identificador do usuário.

        Returns:
            Response:
                - 200 OK: Usuário atualizado
                - 400 Bad Request: Dados inválidos
                - 404 Not Found: Usuário não encontrado
        """
        try:
            user = get_object_or_404(User, pk=pk)
            
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Atualizar Usuário",
                status="SUCCESS",
                message=f"Usuário {pk} atualizado com sucesso"
            )
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Atualizar Usuário",
                status="ERROR",
                message=f"Erro ao atualizar usuário {pk}: {str(e)}"
            )
            return Response(
                {"detail": "Erro ao atualizar usuário"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class UserDeleteView(APIView):
    """
    View responsável por excluir um usuário do sistema.

    A exclusão é realizada com base no identificador do usuário
    informado na URL. Este endpoint não recebe corpo de requisição
    e não utiliza serializer, pois não há dados a serem validados
    ou serializados.

    Endpoint:
        DELETE /api/user/{id}/delete/
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request: Request, pk:int) -> Response:
        """
        Exclui o usuário identificado pelo ID informado.

        Args:
            request (Request): Requisição HTTP.
            pk (int): Identificador do usuário a ser removido.

        Returns:
            Response:
                - 204 No Content: Usuário excluído com sucesso
                - 404 Not Found: Usuário não encontrado
        """
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Excluir Usuário",
                status="SUCCESS",
                message=f"Usuário {pk} excluído com sucesso"
            )
            return Response(
                {"detail": "Usuário excluído com sucesso"},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Excluir Usuário",
                status="ERROR",
                message=f"Erro ao excluir usuário {pk}: {str(e)}"
            )
            return Response(
                {"detail": "Erro ao excluir usuário"},
                status=status.HTTP_400_BAD_REQUEST
            )