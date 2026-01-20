from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de saída do usuário.

    Utilizado exclusivamente para leitura e resposta da API,
    garantindo que informações sensíveis, como a senha, nunca
    sejam expostas.
    """
    class Meta:
        """
        Metadados do serializer UserSerializer.

        Define os campos públicos retornados nas respostas
        relacionadas a usuários.
        """
        model = User
        fields = ["id", "username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela criação de novos usuários.

    Este serializer utiliza o método apropriado do Django
    para criação de usuários, garantindo que a senha seja
    corretamente armazenada utilizando hash.

    Campos esperados:
        - username
        - email
        - password
    """
    
    password = serializers.CharField(write_only=True)
    
    
    is_staff = serializers.BooleanField(required=False, default=False)
    is_superuser = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        """
        Metadados do serializer UserCreateSerializer.
        """
        model = User
        fields = [
            "username",
            "email",
            "password",
            "is_staff",
            "is_superuser",
        ]
        
    def create(self, validated_data):
        """
        Cria e retorna uma nova instância de usuário.

        Este método garante o uso de `create_user`, assegurando
        que a senha seja tratada corretamente pelo sistema
        de autenticação do Django.

        Parameters
        ----------
        validated_data : dict
            Dados validados da requisição.

        Returns
        -------
        User
            Instância do usuário criado.
        """
        password = validated_data.pop("password")
        is_staff = validated_data.pop("is_staff", False)
        is_superuser = validated_data.pop("is_superuser", False)

        # 🔐 Criação correta conforme o tipo
        if is_superuser:
            user = User.objects.create_superuser(
                password=password,
                **validated_data
            )
            return user

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        if is_staff:
            user.is_staff = True
            user.save()

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer responsável pela atualização de dados do usuário.

    Permite atualização parcial dos campos do usuário, incluindo
    alteração opcional de senha. Caso a senha seja fornecida, ela
    é corretamente convertida para hash antes de ser persistida.

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
        """
        Metadados do serializer UserUpdateSerializer.
        """
        model = User
        fields = ["username", "email", "password"]
        
    def update(self, instance, validated_data):
        """
        Atualiza e retorna a instância do usuário.

        Responsabilidades:
        - Atualizar campos simples do usuário
        - Tratar corretamente a alteração de senha
        - Persistir as alterações no banco de dados

        Parameters
        ----------
        instance : User
            Instância do usuário a ser atualizada.
        validated_data : dict
            Dados validados da requisição.

        Returns
        -------
        User
            Instância do usuário atualizada.
        """
        password = validated_data.pop("password", None)
        
        # Atualiza campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Atualiza a senha, se informada   
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance