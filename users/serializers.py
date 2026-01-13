from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de saída do usuário (NUNCA expõe senha).
    """
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela criação de usuários.

    Campos:
        - username
        - email
        - password
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        
    def create(self, validated_data):
        """
        Cria um usuário utilizando o método correto do Django,
        garantindo que a senha seja armazenada com hash.
        """
        user = User.objects.create_user(
            username= validated_data["username"],
            email = validated_data.get("email", ""),
            password = validated_data["password"]
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela atualização de dados do usuário.

    Permite a atualização parcial dos campos, incluindo alteração
    opcional de senha. Caso a senha seja enviada, ela é corretamente
    convertida para hash antes de ser persistida.

    Campos aceitos:
        - username (opcional)
        - email (opcional)
        - password (opcional)
    """
    
    password = serializers.CharField(
        write_only=True,
        required=False
    )
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        
    def update(self, instance, validated_data):
        """
        Atualiza e retorna a instância do usuário.

        Args:
            instance (User): Usuário a ser atualizado.
            validated_data (dict): Dados validados da requisição.

        Returns:
            User: Instância do usuário atualizada.
        """
        password = validated_data.pop("password", None)
        
        # Atualiza campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance