from django.urls import path

from users.views import UserCreateView, UserDeleteView, UserDetailView, UserListView, UserUpdateView

urlpatterns = [
    # LISTAR usuários
    # GET /api/user/
    path("user/", UserListView.as_view(), name="user-list"),
    
    # CRIAR usuário
    # POST /api/user/
    path("user/", UserCreateView.as_view(), name="user-create"),
    
    # CONSULTAR usuário por ID
    # GET /api/user/{id}/
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    
    # ATUALIZAR usuário
    # PUT /api/user/{id}/
    path("user/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    
    # EXCLUIR usuário
    # DELETE /api/user/{id}/
    path("user/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
]