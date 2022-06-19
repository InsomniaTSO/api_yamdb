from django.urls import include, path
from .views import SignupView, UserViewSet, TokenAPIView
from rest_framework.routers import DefaultRouter

from .views import (
    CommentsViewSet,
    ReviewViewSet,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

user_router = DefaultRouter()
user_router.register('users', UserViewSet, basename='user')
models_router = DefaultRouter()
models_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
models_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
models_router.register('categories', CategoryViewSet, basename='category')
models_router.register('genres', GenreViewSet, basename='genre')
models_router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(user_router.urls)),
    path('v1/', include(models_router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
]
