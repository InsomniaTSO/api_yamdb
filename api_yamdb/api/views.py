from multiprocessing import AuthenticationError
from re import T
from requests import request
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from titles.models import Comment, Review
from .permissions import IsSelfOrAdmin, IsAdmin, IsAdminModerOrSelf
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    UserSerializer,
    SignupSerializer,
    TokenSerializer
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
    permission_classes=(IsAdmin,)
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
            serializer = self.get_serializer(user, data=request.data, partial=True)
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
        email_body = 'Здравствуйте '+ user.username + \
            f' Используйте код ниже чтобы варифицировать вашу почту \n' + user.confirmation_code
        send_mail('Verify your email', email_body, 'from@example.com',
                [user.email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

