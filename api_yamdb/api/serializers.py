import json
from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

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
    
    def validate(self, attrs):
        user = self.context['request'].user
        if 'role' in attrs and user.role == 'user':
            role=attrs.pop('role')
        return attrs


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
            is_active=True
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
        user = get_object_or_404(User, username=username)
        attrs.update({'password': ''})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код')
        attrs = json.loads(json.dumps(attrs))
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass
        self.user = User.objects.get(username=authenticate_kwargs['username'])
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        refresh = self.get_token(self.user)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return {'token': str(refresh.access_token)}