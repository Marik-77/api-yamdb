from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api.utils import (CAT_GENRE_NAME, EMAIL_MAX_LENGTH, LIMIT, MAX_LENGTH_255,
                       MAX_SCORE, MIN_SCORE, NAME_MAX_LENGTH)
from reviews.validators import validate_username, validate_year

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        verbose_name='юзернейм',
        max_length=NAME_MAX_LENGTH,
        validators=[validate_username],
        unique=True)
    email = models.EmailField(
        verbose_name='почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True)
    role = models.CharField(
        choices=CHOICES,
        max_length=MAX_LENGTH_255,
        default=USER)
    bio = models.TextField('Биография', blank=True)
    first_name = models.CharField(
        verbose_name='Имя', max_length=NAME_MAX_LENGTH,)
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=NAME_MAX_LENGTH,)

    class Meta:
        ordering = ['username',]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class AbstractModel(models.Model):
    name = models.CharField(
        max_length=CAT_GENRE_NAME,
        verbose_name='Имя категории')
    slug = models.SlugField(
        unique=True,
        verbose_name='слаг категории')

    def __str__(self):
        return self.slug

    class Meta:
        abstract = True
        ordering = ['name',]


class Category(AbstractModel):
    class Meta(AbstractModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractModel):
    class Meta(AbstractModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):

    name = models.TextField(verbose_name='Название произведения')
    year = models.SmallIntegerField(
        verbose_name='Год выхода',
        validators=[validate_year],
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(Genre,
                                   verbose_name='жанр')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-year']

    def __str__(self):
        return self.name


class CommentReviewAbstractModel(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        default=timezone.now,
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date',]


class Review(CommentReviewAbstractModel):
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                MIN_SCORE,
                message=f'Оценка не может быть меньше {MIN_SCORE}'),
            MaxValueValidator(
                MAX_SCORE,
                message=f'Оценка не может быть больше {MAX_SCORE}')
        ],
    )

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        blank=True
    )

    class Meta(CommentReviewAbstractModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_follow'
            ),)

    def __str__(self):
        return (f'Отзыв {self.author.username}'
                f' на {self.title.name}: ({self.score}/10)')


class Comment(CommentReviewAbstractModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )

    class Meta(CommentReviewAbstractModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'коммент'
        verbose_name_plural = 'комменты'

    def __str__(self):
        return (f'Коммент {self.author.username}'
                f' к обзору "{self.review.text[:LIMIT]}" ')
