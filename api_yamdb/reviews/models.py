from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


User = get_user_model()


class Review(models.Model):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(
        'titles.Title',  # Ленивое обращение к модели Title в другом приложении
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
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10'),
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публицации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_per_title_author'
            )
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'

    def save(self, *args, **kwargs):
        """Сохраняет отзыв и обновляет рейтинг произведения."""
        super().save(*args, **kwargs)
        self._update_title_rating()

    def delete(self, *args, **kwargs):
        """Удаляет отзыв и обновляет рейтинг произведения."""
        title_id = self.title_id
        super().delete(*args, **kwargs)
        self._update_title_rating(title_id)

    def _update_title_rating(self, title_id=None):
        """Обновляет рейтинг произведения."""
        if title_id is None:
            title_id = self.title_id
        avg_result = Review.objects.filter(
            title_id=title_id
        ).aggregate(avg_score=Avg('score'))

        avg_score = avg_result['avg_score']
        if avg_score is not None:
            rating_value = round(avg_score)
        else:
            rating_value = None

        title_model = apps.get_model('titles', 'Title')
        title_model.objects.filter(pk=title_id).update(rating=rating_value)


class Comment(models.Model):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review.id}'
