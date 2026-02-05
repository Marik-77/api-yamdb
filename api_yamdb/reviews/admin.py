from api.utils import LIMIT
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    ordering = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'display_genre')
    list_filter = ('year', 'category')
    list_editable = ('category',)
    list_display_links = ('id', 'name')

    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'review',
        'pub_date',
        'display_text_preview')
    search_fields = ('text', 'author__username', 'review__text')
    list_filter = ('pub_date', 'author')

    def display_text_preview(self, obj):
        if len(obj.text) > LIMIT:
            return f"{obj.text[:LIMIT]}..."
        return obj.text
    display_text_preview.short_description = 'Текст'
