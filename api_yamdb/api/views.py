from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from users.models import User
from titles.models import Comment, Review, Title
from .permissions import IsSelf, IsAdmin, IsAdminModerOrSelf
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModerOrSelf,)

    def title_object(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.title_object()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.title_object()
        serializer.save(
            author=self.request.user,
            title=title
        )

    def perform_destroy(self, instance):
        title = self.title_object()
        review_id = self.kwargs.get('pk')
        review = get_object_or_404(Review, title=title, id=review_id)
        review.delete()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModerOrSelf,)

    def review_object(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return get_object_or_404(Review, title=title)

    def get_queryset(self):
        review = self.review_object()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.review_object()
        serializer.save(
            author=self.request.user,
            review=review
        )

    def perform_destroy(self, instance):
        review = self.review_object()
        comment_id = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, review=review, id=comment_id)
        comment.delete()


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
