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