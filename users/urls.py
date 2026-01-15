"""
Rotas responsáveis pelo gerenciamento de usuários do sistema.
Este módulo define endpoints para criação, listagem,
consulta, atualização e exclusão de usuários, delegando
toda a lógica de negócio para as respectivas views.
"""
from django.urls import path
from users.views import UserDetailView,UserView

urlpatterns = [
    # LISTAR e CRIAR usuários
    # GET  /api/user/
    # POST /api/user/
    path("user/", UserView.as_view(), name="user"),

    # CONSULTAR, ATUALIZAR e EXCLUIR usuário
    # GET    /api/user/{id}/
    # PUT    /api/user/{id}/
    # DELETE /api/user/{id}/
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]