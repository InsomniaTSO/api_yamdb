from django.db import router
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, CategoryViewSet, GenreViewSet

user_router = DefaultRouter()
router = DefaultRouter()
user_router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
urlpatterns = [
    path('v1/users', include(user_router.urls)),
    path('v1/', include(router.urls)),
]
