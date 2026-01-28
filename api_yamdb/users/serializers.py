from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Минимальный сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        read_only_fields = ('role',)  # роль нельзя менять через /users/me/
