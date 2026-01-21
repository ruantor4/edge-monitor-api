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
    View responsável por manipular o recurso USUÁRIO conforme o padrão REST.

    Esta view trata operações sobre a coleção de usuários,
    permitindo listagem e criação de novos registros.

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

        Responsabilidades:
        - Recuperar usuários persistidos
        - Serializar os dados para resposta
        - Registrar a operação em log

        Returns
        -------
        Response
            - 200 OK: Lista de usuários
            - 500 Internal Server Error: Erro inesperado
        """
        try:
            users = User.objects.all().order_by("id")
            serializer = UserSerializer(users, many=True)
            
            report_log(
                    user=request.user,
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
                user=request.user,
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

        Responsabilidades:
        - Validar dados de entrada
        - Criar usuário utilizando serializer dedicado
        - Registrar operação em log

        Returns
        -------
        Response
            - 201 Created: Usuário criado com sucesso
            - 400 Bad Request: Dados inválidos
            - 500 Internal Server Error: Erro inesperado
        """
        actor = request.user
        
        # User comum não cria ninguém
        if not actor.is_staff:
            return Response(
                {"detail": "Você não tem permissão para criar usuários"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Admin NÃO pode criar root
        if (
            actor.is_staff
            and not actor.is_superuser
            and request.data.get("is_superuser") is True
        ):
            return Response(
                {"detail": "Administrador não pode criar usuário root"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            serializer = UserCreateSerializer(
            data=request.data,
            context={"request": request}
        )
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

    Esta classe centraliza operações de consulta, atualização
    e exclusão de usuários, mantendo todas as ações relacionadas
    a um único recurso sob o mesmo endpoint.

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

        Responsabilidades:
        - Recuperar o usuário pelo identificador
        - Serializar os dados para resposta
        - Registrar a operação em log

        Returns
        -------
        Response
            - 200 OK: Dados do usuário
            - 404 Not Found: Usuário não encontrado
        """
        try:
            user = get_object_or_404(User, pk=pk)
            
            report_log(
                user=request.user,
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
                user=request.user,
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

        Responsabilidades:
        - Validar dados recebidos
        - Atualizar campos permitidos
        - Registrar operação em log

        Returns
        -------
        Response
            - 200 OK: Usuário atualizado
            - 400 Bad Request: Dados inválidos
        """
        actor = request.user
        target = get_object_or_404(User, pk=pk)

        # Superuser pode editar tudo
        if actor.is_superuser:
            pass

        # Admin (staff)
        elif actor.is_staff:
            if target.is_superuser:
                return Response(
                    {"detail": "Administrador não pode editar superusuário"},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Usuário comum
        else:
            if target.id != actor.id:
                return Response(
                    {"detail": "Você só pode editar o próprio usuário"},
                    status=status.HTTP_403_FORBIDDEN
                )

        try:
            serializer = UserUpdateSerializer(
                target,
                data=request.data,
                partial=True,
                context={"request": request}
            )
            
            serializer.is_valid(raise_exception=True)
            serializer.save()

            report_log(
                user=actor,
                action="Atualizar Usuário",
                status="SUCCESS",
                message=f"Usuário {pk} atualizado"
            )

            return Response(
                UserSerializer(target).data,
                status=status.HTTP_200_OK
            )

        except ValidationError as exc:
            return Response(
                exc.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            report_log(
                user=actor,
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

        Responsabilidades:
        - Remover o usuário identificado
        - Tratar vínculos e restrições de integridade
        - Registrar operação em log

        Returns
        -------
        Response
            - 204 No Content: Usuário excluído
            - 409 Conflict: Usuário possui vínculos
            - 500 Internal Server Error: Erro inesperado
        """
        actor = request.user
        target = get_object_or_404(User, pk=pk)

        # Superuser nunca pode ser excluído
        if target.is_superuser:
            return Response(
                {"detail": "Usuário root não pode ser excluído"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Superuser pode excluir qualquer outro
        if actor.is_superuser:
            pass

        # Admin
        elif actor.is_staff:
            pass  # pode excluir user comum e admin

        # Usuário comum
        else:
            return Response(
                {"detail": "Você não tem permissão para excluir usuários"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            target.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except IntegrityError:
            return Response(
                {"detail": "Usuário possui registros vinculados"},
                status=status.HTTP_409_CONFLICT
            )
        
        except Exception as e:
            report_log(
                user=request.user,
                action="Excluir Usuário",
                status="ERROR",
                message=f"Erro ao excluir usuário: {str(e)}"
            )
            return Response(
                {"detail": "Erro interno ao excluir usuário"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
