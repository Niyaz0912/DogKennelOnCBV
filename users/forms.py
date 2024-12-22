from django import forms

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from users.models import User
from users.validators import validate_password


class StyleFormMixin:
    """
    Миксин для добавления стилей к формам.

    Этот класс добавляет класс 'form-control' ко всем полям формы при инициализации.

    Атрибуты:
        *args: Позиционные аргументы для инициализации родительского класса.
        **kwargs: Ключевые аргументы для инициализации родительского класса.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Применение класса к каждому полю формы


class UserForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для обновления данных пользователя.

    Эта форма позволяет редактировать информацию о пользователе, такую как email, имя и телефон.

    Метаданные:
        Meta: Определяет модель и поля, которые будут включены в форму.
    """

    class Meta:
        model = User  # Модель пользователя
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar',)  # Поля для редактирования


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма регистрации нового пользователя.

    Эта форма позволяет создать нового пользователя с проверкой пароля.

    Метаданные:
        Meta: Определяет модель и поля, которые будут включены в форму.
    """

    class Meta:
        model = User  # Модель пользователя
        fields = ('email',)  # Поля для регистрации

    def clean_password2(self):
        """
        Проверяет совпадение паролей и применяет пользовательскую валидацию пароля.

        Raises:
            ValidationError: Если пароли не совпадают или не проходят валидацию.

        Returns:
            str: Второй пароль, если он валиден.
        """
        temp_data = self.cleaned_data
        validate_password(temp_data['password1'])  # Валидация первого пароля
        if temp_data['password1'] != temp_data['password2']:
            raise forms.ValidationError('password_mismatch')  # Ошибка при несовпадении паролей
        return temp_data['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для аутентификации пользователя.

    Позволяет пользователю вводить свои учетные данные для входа в систему.
    """
    pass  # Использует стандартные функции AuthenticationForm


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для обновления информации о пользователе.

    Эта форма позволяет редактировать информацию о пользователе, такую как email и номер телефона.

    Метаданные:
        Meta: Определяет модель и поля, которые будут включены в форму.
    """

    class Meta:
        model = User  # Модель пользователя
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar',)  # Поля для редактирования


class UserPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    """
    Форма для изменения пароля пользователя.

    Эта форма позволяет пользователю изменить свой пароль с проверкой на соответствие новым требованиям.

    Методы:
        clean_new_password2(): Проверяет новый пароль на совпадение и валидность.

    Returns:
         str: Новый пароль, если он валиден.
     """

    def clean_new_password2(self):
        """
        Проверяет совпадение новых паролей и применяет пользовательскую валидацию пароля.

        Raises:
            ValidationError: Если пароли не совпадают или не проходят валидацию.

        Returns:
            str: Второй новый пароль, если он валиден.
        """
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        validate_password(password1)  # Валидация нового пароля
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.user)  # Стандартная валидация пароля
        return password2
