from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ACCESS_ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]

    class Meta:
        ordering = ('username',)

    username = models.CharField(db_index=True,
                                max_length=150,
                                unique=True)
                               
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True 
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True 
    )

    role = models.CharField(
        'Роль',
        max_length=150,
        choices=ACCESS_ROLE,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    confirmation_code = models.CharField(
        'Код поддтверждения',
        max_length=150,
        blank=True 
    )

    def __str__(self):
        return self.username
