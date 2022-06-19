from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filter import TitleFilter
from users.models import User
from .permissions import (
    IsSelfOrAdmin,
    IsAdmin,
    IsAdminModerOrSelf,
    IsAdminOrReadOnly
)
from titles.models import Comment, Review, Title, Category, Genre
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    SignupSerializer,
    TokenSerializer,
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


class UserViewSet (viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(methods=['get', 'patch'],
            detail=False,
            url_name='me',
            url_path='me',
            permission_classes=(IsSelfOrAdmin,))
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignupView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(username=user_data['username'])
        email_body = 'Здравствуйте ' + user.username + \
            f' Используйте код ниже чтобы варифицировать вашу почту \n' + user.confirmation_code
        send_mail('Verify your email', email_body, 'from@example.com',
                  [user.email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class TitleViewSet(CustomViewSet):
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer
