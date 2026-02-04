from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model() #В последующем будет использоваться кастомная модель User

class Review(models.Model):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(
        Title,  # Модель описана разработчиком 2
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Напишите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        MinValueValidator(
            1,
            message='Оценка не может быть меньше 1'
        ),
        MaxValueValidator(
            10,
            message='Оценка не может быть больше 10'
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публицации',
        auto_now_add=True
    )