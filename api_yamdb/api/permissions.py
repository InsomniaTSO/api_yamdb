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
        if (request.user and request.user.is_authenticated):
            return (request.user.role == 'admin'
                    or request.user.is_superuser
                    )
        return False

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or request.user.is_superuser)


class IsSelfOrAdmin(permissions.BasePermission):
    """Разрешение на редактирование только владельцем и админом"""

    message = 'Доступ только у владельца!'

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj == request.user
                or request.user.role == 'admin'
                )


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только автору."""
    message = 'Доступ только у автора!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только админу, остальным только чтение."""
    message = 'Доступ на только у автора!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))


class ReadOnlyForUnauthorized(permissions.BasePermission):
    """Разрешение на отправку SAFE-методов любому пользователю."""
    message = 'Вы не авторизованы!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin')
