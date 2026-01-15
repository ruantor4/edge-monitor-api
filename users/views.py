from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from core.utils import report_log
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)

class UserView(APIView):
    """
    View responsável por manipular o recurso USUÁRIO conforme o padrão REST
    

    Endpoints atendidos:
        - GET  /api/user/   → Listar usuários
        - POST /api/user/   → Criar usuário
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses=UserSerializer(many=True)
    )
    def get(self, request: Request) -> Response:
        """
        Lista todos os usuários cadastrados no sistema.

        Endpoint:
            GET /api/user/

        Returns:
            - 200 OK: Lista de usuários
            - 500 Internal Server Error
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
    
    @extend_schema(
        request=UserCreateSerializer,
        responses=UserSerializer
    )        
    def post(self, request: Request) -> Response:
        """
        Cria um novo usuário no sistema.

        Endpoint:
            POST /api/user/

        Body:
            - username
            - email
            - password

        Returns:
            - 201 Created: Usuário criado
            - 400 Bad Request: Dados inválidos
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

        except ValidationError as exc:
            return Response(
                exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError:
            return Response(
                {"detail": "Dados inválidos ou duplicados"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exc:
            return Response(
                {"detail": "Erro interno do servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDetailView(APIView):
    """
    View responsável por manipular um usuário específico.

    🔴 ALTERAÇÃO ESTRUTURAL:
    -----------------------
    Esta classe UNIFICA:
        - UserDetailView (GET)
        - UserUpdateView (PUT)
        - UserDeleteView (DELETE)

    Endpoint base:
        /api/user/{id}/
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses=UserSerializer
    )
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
    
    
    @extend_schema(
        request=UserUpdateSerializer,
        responses=UserSerializer
    )        
    def put(self, request: Request, pk: int) -> Response:
        """
        Atualiza os dados de um usuário existente.

        Endpoint:
            PUT /api/user/{id}/
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
                user=request.user,
                action="Atualizar Usuário",
                status="SUCCESS",
                message=f"Usuário {pk} atualizado"
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
                message=f"Erro ao atualizar usuário: {str(e)}"
            )
            return Response(
                {"detail": "Erro ao atualizar usuário"},
                status=status.HTTP_400_BAD_REQUEST
            )


    @extend_schema(
        responses={204: None, 404: None, 409: None, 500: None}
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Exclui um usuário do sistema.

        Endpoint:
            DELETE /api/user/{id}/
        """
        user = get_object_or_404(User, pk=pk)
        
        try:    
            user.delete()

            report_log(
                user=request.user,
                action="Excluir Usuário",
                status="SUCCESS",
                message=f"Usuário {pk} excluído"
            )

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        
        except IntegrityError:
            report_log(
                user=request.user,
                action="Excluir Usuário",
                status="WARNING",
                message=f"Usuário {pk} possui vínculos e não pode ser excluído"
            )
            return Response(
                {"detail": "Usuário possui registros vinculados"},
                status=status.HTTP_409_CONFLICT
            )
        
        except Exception as e:
            report_log(
                user=request.user if request.user.is_authenticated else None,
                action="Excluir Usuário",
                status="ERROR",
                message=f"Erro ao excluir usuário: {str(e)}"
            )
            return Response(
                {"detail": "Erro interno ao excluir usuário"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
