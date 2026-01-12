from django.urls import path

from users.views import UserCreateView, UserListView

urlpatterns = [
    path("user/", UserListView.as_view(), name="user-list"),
    path("user/create/", UserCreateView.as_view(), name="user-create"),
    
]