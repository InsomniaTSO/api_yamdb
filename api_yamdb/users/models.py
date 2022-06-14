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

    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ACCESS_ROLE,
        default=USER,
    )
