from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=1,
        max_length=150,
        help_text="Имя пользователя от 1 до 150 символов"
    )
    email = serializers.EmailField(
        max_length=254,
        help_text="Email пользователя (не более 254 символов)"
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Использовать имя пользователя 'me' запрещено."
            )
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Допустимы только буквы, цифры и символы: @/./+/-/_"
            )
        return value

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username:
            if user_by_username.email == email:
                attrs['user_instance'] = user_by_username
                return attrs
            else:
                raise serializers.ValidationError({
                    "username": (
                        "Этот username уже зарегистрирован, "
                        "нельзя использовать другой email."
                    )
                })

        if user_by_email:
            raise serializers.ValidationError({
                "email": "Этот email уже зарегистрирован другим пользователем."
            })

        attrs['user_instance'] = None
        return attrs


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value):
        allowed_roles = [User.USER, User.MODERATOR, User.ADMIN]
        if value not in allowed_roles:
            raise serializers.ValidationError("Некорректная роль.")
        return value

    def create(self, validated_data):
        if 'role' not in validated_data or validated_data['role'] is None:
            validated_data['role'] = User.USER
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        role = validated_data.get('role')

        if role and request and request.user.is_staff:
            self.validate_role(role)
            instance.role = role

        for attr, value in validated_data.items():
            if attr != 'role':
                setattr(instance, attr, value)

        instance.save()
        return instance
