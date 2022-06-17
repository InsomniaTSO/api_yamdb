from rest_framework import serializers
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from titles.models import Comment, Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username',
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
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )  

    def validate_username(self, username):
        if 'me' == username.lower():
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено!'
            )
        return username


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""

    class Meta:
        model = User
        fields = ['username', 'email',]

    def validate_username(self, username):
        if 'me' == username.lower():
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено!'
            )
        return username
    
    def validate_password(self, password):
        return make_password(password)

    def create(self, validated_data):
        confirmation_code = BaseUserManager().make_random_password()
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            confirmation_code=confirmation_code,
        )
        user.save()
        return user


class TokenSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        username=attrs.get('username')
        confirmation_code=attrs.pop('confirmation_code')
        user = User.objects.get(username=username)
        attrs.update({'password': ''})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код')
        return super(TokenSerializer, self).validate(attrs)
