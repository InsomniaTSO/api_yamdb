from multiprocessing import AuthenticationError
from rest_framework import permissions


SAFE_ROLE = ['admin', 'moderator']


class ReadOnly(permissions.BasePermission):
    """Разрешение на чтение любым пользователем."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminModerOrSelf(permissions.BasePermission):
    """Разрешение на редактирование только автором, модератором или админом."""
    message = 'Изменение и удаление чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in SAFE_ROLE
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Разрешение на редактирование только админом."""
    message = 'Доступ только у администаратора!'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationError(
                'Пользователь не авторизован'
            )
        return (request.user.role == 'admin' 
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin' 
                or request.user.is_superuser)


class IsSelf(permissions.BasePermission):
    """Разрешение на редактирование только владельцем."""
    message = 'Доступ только у владельца!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj == request.user)


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только автору."""
    message = 'Доступ только у автора!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
