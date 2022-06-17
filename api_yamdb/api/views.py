from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action

from users.models import User
from titles.models import Comment, Review, Title, Category, Genre
from .permissions import IsSelf, IsAdmin, IsAdminModerOrSelf
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleReadSerializer
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    @action(methods=['get', 'patch'],
            detail=False,
            url_name='me',
            url_path='me',
            permission_classes=[IsSelf])
    def me(self, request, pk=None):
        user = self.request.user
        return user


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class TitleViewSet(CustomViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer
