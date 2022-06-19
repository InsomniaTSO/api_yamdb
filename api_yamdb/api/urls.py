from django.urls import include, path
from .views import SignupView, UserViewSet, TokenAPIView
from rest_framework.routers import DefaultRouter

user_router = DefaultRouter()
user_router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/', include(user_router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
]
