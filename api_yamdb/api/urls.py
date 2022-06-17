from django.urls import include, path
from .views import SignupView, UserViewSet, TokenAPIView
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenAPIView.as_view(), name='token'),
]
