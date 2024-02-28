from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    confirmation_code = models.CharField(
        max_length=100,
        blank=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Введите адрес эл.почты',
        unique=True
    )
    bio = models.TextField(
        verbose_name='О пользователе',
        help_text='Расскажите о себе',
        blank=True,
        null=True
    )

    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        choices=USER_ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
