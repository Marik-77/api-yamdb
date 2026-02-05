from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthorReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование/удаление.

    Редактировать и удалять может только автор объекта.
    Модераторы и администраторы имеют полный доступ.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
            obj.author == user
            or getattr(user, 'is_admin', False)
            or getattr(user, 'is_moderator', False)
        )
    

class IsReviewAuthorOrReadOnly(IsAuthorReadOnly):
    """Для отзывов - проверяем автора отзыва."""


class IsCommentAuthorOrReadOnly(IsAuthorReadOnly):
    """Для комментариев - проверяем автора комментария."""