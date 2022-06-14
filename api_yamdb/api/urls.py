from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

user_router = DefaultRouter()
user_router.register('users', UserViewSet, basename='user')
urlpatterns = [
    path('v1/users', include(user_router.urls)),
]
