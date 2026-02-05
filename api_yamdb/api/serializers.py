import datetime
import re

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (ADMIN, MODERATOR, USER, Category, Comment, Genre,
                            Review, Title, User)

from .mixins import ValidateUsername
from .utils import (EMAIL_MAX_LENGTH, MAX_LENGTH_255, NAME_MAX_LENGTH,
                    PATTERN_SLUG, SLUG_LEN)


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    username = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True)
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    first_name = serializers.CharField(
        max_length=NAME_MAX_LENGTH,
        required=False)
    last_name = serializers.CharField(
        max_length=NAME_MAX_LENGTH,
        required=False)
    role = serializers.CharField(max_length=MAX_LENGTH_255, default='user')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_role(self, value):
        if value in (ADMIN, USER, MODERATOR):
            return value
        raise serializers.ValidationError(['Нет такой роли!'])

    def validate_email(self, value):
        view = self.context.get('view')

        if view:
            username_from_url = view.kwargs.get('username')
            user_from_url = User.objects.filter(
                email=value, username=username_from_url
            )
            if user_from_url.exists():
                return value

        user = User.objects.filter(
            email=value
        )
        if user.exists():
            raise serializers.ValidationError(
                ['email уже занят']
            )
        return value

    def validate(self, data):
        user = User.objects.filter(
            username=data.get('username')
        )
        if user.exists():
            raise serializers.ValidationError(
                ['username уже занят']
            )
        return data


class RegisterSerializer(serializers.Serializer, ValidateUsername):
    username = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True)
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)

    def validate(self, data):

        email = data.get('email')
        username = data.get('username')
        data['exists'] = False
        user = User.objects.filter(
            username=username, email=email
        )
        if user.exists():
            user = User.objects.get(
                username=username, email=email
            )
            token = default_token_generator.make_token(user)
            data['token'] = token
            data['exists'] = True
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                ["Пользователь с таким именем уже существует."])
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                ["Пользователь с такой почтой уже существует."])
        data['exists'] = False
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True)
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_255,
        required=True)

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate(self, data):

        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError({
                "confirmation_code": ['Невереный confirmation_code']
            })
        data['user'] = user

        return data


class CatGenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=SLUG_LEN,
        required=True)

    class Meta:
        abstract = True
        fields = ('name', 'slug')


class CategorySerializer(CatGenreSerializer):

    class Meta(CatGenreSerializer.Meta):
        model = Category

    def validate_slug(self, value):
        category = Category.objects.filter(
            slug=value
        )
        if category.exists():
            raise serializers.ValidationError(
                ['Такая категория уже есть']
            )
        if re.match(PATTERN_SLUG, value):
            return value
        raise serializers.ValidationError(
            ['Неправильный slug']
        )


class GenreSerializer(CatGenreSerializer):

    class Meta(CatGenreSerializer.Meta):
        model = Genre

    def validate_slug(self, value):
        genre = Genre.objects.filter(
            slug=value
        )
        if genre.exists():
            raise serializers.ValidationError(
                ['Такой жанр уже есть']
            )
        if re.match(PATTERN_SLUG, value):
            return value
        raise serializers.ValidationError(
            ['Неправильный slug']
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category',
                  )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True,
    )
    genre = serializers.SlugRelatedField(
        required=True,
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        allow_null=False
    )
    name = serializers.CharField(max_length=256, required=True)
    year = serializers.IntegerField(
        required=True, max_value=datetime.date.today().year)

    class Meta:
        model = Title
        fields = ('id', 'category', 'genre', 'name', 'year', 'description', )

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        view = self.context.get('view')

        if request and view:
            title_id = view.kwargs.get('title_id')

            if Review.objects.filter(
                author=request.user,
                title_id=title_id
            ).exists() and request.method == 'POST':
                raise serializers.ValidationError(
                    ['Вы уже оставляли отзыв на это произведение.']
                )

        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
