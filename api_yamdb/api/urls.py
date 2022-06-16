from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentsViewSet, ReviewViewSet, UserViewSet

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


urlpatterns = [
    path('v1/users', include(user_router.urls)),
    path('v1/', include(models_router.urls)),
]
