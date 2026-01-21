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
        fields = [
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
        ]


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
     
    def validate(self, attrs):
        """
        Valida permissões para criação de usuários.

        Responsabilidades:
        - Impedir criação por usuário comum
        - Impedir administrador de criar superusuário
        """
        request = self.context.get("request")
        actor = request.user if request else None

        # Usuário comum não cria ninguém
        if not actor or not actor.is_staff:
            raise serializers.ValidationError(
                "Você não tem permissão para criar usuários"
            )
            
        # Admin não pode criar superuser
        if (
            actor.is_staff
            and not actor.is_superuser
            and attrs.get("is_superuser") is True
        ):
            raise serializers.ValidationError(
                "Administrador não pode criar superusuário"
            )

        return attrs

    def create(self, validated_data):
        """
        Cria e retorna uma nova instância de usuário.
        """
        password = validated_data.pop("password")
        is_staff = validated_data.pop("is_staff", False)
        is_superuser = validated_data.pop("is_superuser", False)

        if is_superuser:
            return User.objects.create_superuser(
                password=password,
                **validated_data
            )

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
    
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)
    
    class Meta:
        """
        Metadados do serializer UserUpdateSerializer.
        """
        model = User
        fields = [
            "username",
            "email",
            "password",
            "is_staff",
            "is_superuser",
        ]
    
    def validate(self, attrs):
        request = self.context.get("request")
        actor = request.user if request else None
        instance = self.instance

        # Alteração de superuser
        if "is_superuser" in attrs:
            if attrs["is_superuser"] != instance.is_superuser:
                if not actor or not actor.is_superuser:
                    raise serializers.ValidationError(
                        "Você não tem permissão para alterar superusuário"
                    )

        # Alteração de staff
        if "is_staff" in attrs:
            if attrs["is_staff"] != instance.is_staff:
                if not actor or not actor.is_staff:
                    raise serializers.ValidationError(
                        "Você não tem permissão para alterar administrador"
                    )

        return attrs
        
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

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance