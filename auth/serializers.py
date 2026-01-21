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
    
class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer responsável por validar a solicitação de
    recuperação de senha.

    Este serializer define o contrato de entrada para o
    endpoint de solicitação de reset de senha via e-mail.

    Responsabilidades:
    - Validar o formato do e-mail informado
    - Servir como contrato explícito para a camada de view

    IMPORTANTE:
    - Não valida se o e-mail existe ou não
    - A view é responsável por tratar esse cenário de forma segura
    """
    
    email = serializers.EmailField(
        help_text="E-mail cadastrado do usuário para recuperação de senha"
    )
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer responsável por validar a confirmação de
    redefinição de senha.

    Utilizado no endpoint que recebe o token de recuperação
    e a nova senha definida pelo usuário.

    Responsabilidades:
    - Validar presença e formato do token
    - Validar nova senha informada
    - Servir como contrato explícito para a camada de view
    """
    uid = serializers.CharField(
        help_text="Identificador codificado do usuário"
    )
    
    token = serializers.CharField(
        help_text="Token de recuperação de senha"
    )
    
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        help_text="Nova senha do usuário"
    )