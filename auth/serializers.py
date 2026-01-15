from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer responsável por representar o payload de autenticação
    de usuários no sistema.

    Este serializer **não está associado a nenhum model** e existe
    exclusivamente para:
        - Validação básica do corpo da requisição de login
        - Documentação do endpoint no Swagger / OpenAPI

    Ele define explicitamente os campos esperados no corpo da
    requisição de autenticação.
    """

    username = serializers.CharField(
        help_text="Nome de usuário cadastrado no sistema"
    )

    password = serializers.CharField(
        help_text="Senha correspondente ao usuário informado",
        write_only=True
    )
    
class RenovateTokenSerializer(serializers.Serializer):
    """
    Payload para renovação do access token.
    """
    renovate = serializers.CharField(
        help_text="Refresh token utilizado para gerar um novo access token"
    )
    
class LogoutSerializer(serializers.Serializer):
    """
    Payload para logout do usuário.
    """
    renovate = serializers.CharField(
        help_text="Refresh token a ser invalidado"
    )