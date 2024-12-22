from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Определяет настройки для полей, которые могут быть пустыми или нулевыми
NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Класс для определения ролей пользователей с использованием текстовых выборов.

    Атрибуты:
        ADMIN (str): Роль администратора.
        MODERATOR (str): Роль модератора.
        USER (str): Роль обычного пользователя.
    """
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель AbstractUser.

    Эта модель заменяет поле username на email и добавляет дополнительные поля,
    такие как роль, телефон, Telegram и аватар.

    Атрибуты:
        username (str): Удалено, так как используется email вместо него.
        email (EmailField): Уникальный адрес электронной почты пользователя.
        role (CharField): Роль пользователя, выбираемая из UserRoles.
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя.
        phone (CharField): Номер телефона пользователя.
        telegram (CharField): Имя пользователя в Telegram.
        avatar (ImageField): Аватар пользователя, загружаемый в папку 'users/'.
        is_active (BooleanField): Статус активности пользователя.

    Методы:
        __str__(): Возвращает строковое представление объекта пользователя по его email.

    Метаданные:
        verbose_name: Человекочитаемое имя модели в единственном числе.
        verbose_name_plural: Человекочитаемое имя модели во множественном числе.
        ordering: Определяет порядок сортировки объектов по id.
    """

    username = None  # Удаление поля username
    email = models.EmailField(unique=True, verbose_name='email')  # Уникальный email
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)  # Роль пользователя
    first_name = models.CharField(max_length=150, verbose_name='First Name', default="Anonymous")  # Имя
    last_name = models.CharField(max_length=150, verbose_name='Last Name', default="Anonymous")  # Фамилия
    phone = models.CharField(max_length=35, verbose_name='Phone Number', **NULLABLE)  # Номер телефона
    telegram = models.CharField(max_length=150, verbose_name='Telegram Username', **NULLABLE)  # Имя в Telegram
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)  # Аватар
    is_active = models.BooleanField(default=True, verbose_name='active')  # Статус активности

    USERNAME_FIELD = "email"  # Установка поля для аутентификации
    REQUIRED_FIELDS = []  # Поля, которые обязательны при создании суперпользователя

    def __str__(self):
        """Возвращает строковое представление объекта пользователя по его email."""
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'Users'  # Человекочитаемое имя модели во множественном числе
        ordering = ['id']  # Порядок сортировки объектов по id
