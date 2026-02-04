from rest_framework import permissions

class IsAuthorReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование/удаление.

    Редактироать и удалять может только автор объекта.
    Можераторы и администраторы имеют полный доступ.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user or
            request.user.is_staff or
            request.user.role in ['admin', 'moderator']
        )
    

class IsReviewAuthorOrReadOnly(IsAuthorReadOnly):
    """Для отзывов - проверяем автора отзыва."""