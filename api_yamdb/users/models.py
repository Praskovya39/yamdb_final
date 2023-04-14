from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
STAFF = 'moderator'
ADMIN = 'admin'

CHOISES = (
    (USER, 'пользователь'),
    (STAFF, 'модератор'),
    (ADMIN, 'администратор')
)


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Имя',
        help_text='Напишите свое имя'
    )
    last_name = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='Фамилия',
        help_text='Напишите свою фамилию',
    )
    bio = models.TextField(
        max_length=500,
        null=True,
        verbose_name='Биография',
        help_text='Расскажите о себе',
    )
    role = models.CharField(
        max_length=15,
        choices=CHOISES,
        default='user',
        verbose_name='Статус пользователя',
    )

    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Проверка пользователя на администратора."""
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка пользователя на модератора."""
        return self.role == STAFF

    @property
    def is_user(self):
        """Проверка пользователя на юзера."""
        return self.role == USER

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('email', 'username'),
                                    name='unique_user'),
        )
