from rest_framework import serializers


from titles.models import Comment, Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.SlugRelatedField(
        slug='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text',
            'author', 'score',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментов"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text',
            'author', 'pub_date',
        )


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
