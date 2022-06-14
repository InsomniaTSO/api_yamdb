from rest_framework import viewsets
from rest_framework.decorators import action

from users.models import User
from api.serializers import UserSerializer
from api.permissions import IsSelf, IsAdmin


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
