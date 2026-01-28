from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator

from users.models import User
from users.serializers import SignUpSerializer, TokenSerializer, UserSerializer

# Регистрация пользователя:
# принимает username и email
#  создаёт пользователя, если его ещё нет
# генерирует confirmation_code через default_token_generator
# возвращает username, email и confirmation_code


class SignUpView(APIView):
    """Регистрация пользователя и выдача confirmation_code."""

    def post(self, request):
        """Создание пользователя и генерация confirmation_code."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )

        # Генерация кода подтверждения через default_token_generator
        confirmation_code = default_token_generator.make_token(user)

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "confirmation_code": confirmation_code
            },
            status=status.HTTP_201_CREATED
        )

# Получение JWT-токена:
# - принимает username и confirmation_code
# - проверяет токен через default_token_generator.check_token()
# - возвращает access-токен (JWT)


class TokenView(APIView):
    """Получение JWT-токена по username и confirmation_code."""

    def post(self, request):
        """Проверка confirmation_code и генерация access-токена."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"error": "Неверный код подтверждения"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Генерация JWT-токена
        token = str(AccessToken.for_user(user))

        return Response({"token": token}, status=status.HTTP_200_OK)


# Просмотр и редактирование профиля текущего пользователя.
# GET - получить данные
# PATCH - обновить данные (кроме роли)
class UserMeView(APIView):
    """Просмотр и редактирование профиля текущего пользователя."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Получение данных текущего пользователя."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Частичное обновление данных текущего пользователя."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
