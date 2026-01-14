from django.urls import path

from auth.views import LoginView, LogoutView, RenovateTokenView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("renovate/", RenovateTokenView.as_view(), name="token-renovate"),
    path("logout/", LogoutView.as_view(), name="logout")
]