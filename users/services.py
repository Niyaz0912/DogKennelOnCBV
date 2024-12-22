from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    """
    Отправляет электронное письмо с подтверждением регистрации.

    Эта функция отправляет пользователю письмо с поздравлением о успешной регистрации на платформе.

    Args:
        email (str): Адрес электронной почты получателя.

    Returns:
        None
    """
    send_mail(
        subject='Поздравляем с регистрацией',  # Тема письма
        message='Вы успешно зарегистрировались на нашей платформе Dog-kennel, добро пожаловать!',  # Сообщение письма
        from_email=settings.EMAIL_HOST_USER,  # Адрес отправителя
        recipient_list=[email]  # Список получателей
    )


def send_new_password(email, new_password):
    """
    Отправляет электронное письмо с новым паролем.

    Эта функция отправляет пользователю письмо с новым паролем после его изменения.

    Args:
        email (str): Адрес электронной почты получателя.
        new_password (str): Новый пароль пользователя.

    Returns:
        None
    """
    send_mail(
        subject='Вы успешно изменили пароль!',  # Тема письма
        message=f'Ваш новый пароль: {new_password}',  # Сообщение письма с новым паролем
        from_email=settings.EMAIL_HOST_USER,  # Адрес отправителя
        recipient_list=[email]  # Список получателей
    )
