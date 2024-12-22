import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    """
    Проверяет, соответствует ли пароль заданным критериям.

    Эта функция проверяет, что пароль содержит только латинские буквы и цифры,
    а также что его длина находится в пределах от 8 до 16 символов.

    Args:
        field (str): Пароль, который необходимо проверить.

    Raises:
        ValidationError: Если пароль не соответствует требованиям.
            - Если пароль содержит недопустимые символы (не латинские буквы или цифры).
            - Если длина пароля не находится в пределах от 8 до 16 символов.

    Returns:
        None
    """
    pattern = re.compile(r'^[A-Za-z0-9]+$')  # Регулярное выражение для проверки символов пароля
    language = settings.LANGUAGE_CODE  # Получение текущего языка из настроек
    error_massages = [
        {
            'ru-ru': 'Пароль должен содержать только символы латинского алфавита и цифры',
            'en-us': 'Must contain A-Z a-z letters and 0-9 numbers'
        },
        {
            'ru-ru': 'Длина пароля должна быть между 8 и 16 символами',
            'en-us': 'Password length must be between 8 and 16 characters'
        }
    ]

    if not bool(re.match(pattern, field)):
        # Если пароль не соответствует регулярному выражению
        print(error_massages[0][language])  # Вывод сообщения об ошибке
        raise ValidationError(
            error_massages[0][language],  # Сообщение об ошибке
            code=error_massages[0][language]  # Код ошибки
        )

    if not 8 <= len(field) <= 16:
        # Если длина пароля не в пределах от 8 до 16 символов
        raise ValidationError(
            error_massages[1][language],  # Сообщение об ошибке
            code=error_massages[1][language]  # Код ошибки
        )
