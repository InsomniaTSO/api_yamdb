from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from users.models import User
from titles.models import Comment, Review
from .permissions import IsSelf, IsAdmin, IsAdminModerOrSelf
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModerOrSelf,)

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        pass

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModerOrSelf,)

    def get_queryset(self):
        pass

    def perform_create(self, serializer):
        pass

    def perform_update(self, serializer):
        pass

    def perform_destroy(self, instance):
        pass


class UserViewSet (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes=[IsAdmin]

    @action(methods=['get', 'patch'],
            detail=False,
            url_name='me',
            url_path='me',
            permission_classes=[IsSelf])
    def me(self, request, pk=None):
        user = self.request.user
        return user
