from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer utilizado para validação do payload de login.

    Esta classe não possui vínculo com models e tem como objetivo
    apenas definir e validar os campos esperados na requisição
    de autenticação de usuários.

    Responsabilidades:
    - Declarar os campos obrigatórios para login
    - Garantir tipagem e presença dos dados
    - Servir como contrato explícito para a camada de view
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
    Serializer responsável por validar o payload de renovação de token.

    Utilizado para garantir a presença do refresh token necessário
    para geração de um novo access token.

    Não executa lógica de renovação, apenas valida o formato dos dados.
    """
    renovate = serializers.CharField(
        help_text="Refresh token utilizado para gerar um novo access token"
    )
    
class LogoutSerializer(serializers.Serializer):
    """
    Serializer responsável por validar o payload de logout.

    Utilizado para garantir que o refresh token a ser invalidado
    seja corretamente informado na requisição.

    Não executa lógica de logout, apenas valida o formato dos dados.
    """
    renovate = serializers.CharField(
        help_text="Refresh token a ser invalidado"
    )