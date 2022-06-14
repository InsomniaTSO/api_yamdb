from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, username):
        if 'me' == username.lower():
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено!'
            )
        return username
