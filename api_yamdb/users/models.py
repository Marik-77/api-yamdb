from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя с ролью, полем bio и уникальным email."""

    # Константы ролей
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    # Варианты ролей
    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    # Роль пользователя
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя'
    )

    # Email должен быть уникальным по ТЗ
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == self.MODERATOR

    def __str__(self):
        """Строковое представление пользователя."""
        return self.username
