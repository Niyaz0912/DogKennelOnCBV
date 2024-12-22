from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from dogs.models import Category


def get_categories_cache():
    """
    Получает список категорий из кеша или базы данных.

    Проверяет, включен ли кеш. Если кеш включен, пытается получить список категорий
    из кеша по ключу 'category_list'. Если список не найден, извлекает его из базы
    данных и сохраняет в кеш. Если кеш отключен, всегда извлекает список категорий
    из базы данных.

    Returns:
        QuerySet: Список всех категорий (Category) из базы данных.
    """
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)  # Попытка получить данные из кеша
        if category_list is None:  # Если данные отсутствуют в кеше
            category_list = Category.objects.all()  # Получение данных из базы
            cache.set(key, category_list)  # Сохранение данных в кеш
    else:
        category_list = Category.objects.all()  # Получение данных из базы, если кеш отключен

    return category_list


def send_views_mail(dog_object, owner_email, views_count):
    """
    Отправляет электронное письмо владельцу собаки о количестве просмотров.

    Использует функцию send_mail для отправки письма с указанием количества
    просмотров записи о собаке. Письмо содержит тему и сообщение с информацией
    о текущем количестве просмотров.

    Args:
        dog_object (Dog): Объект собаки, информация о которой будет включена в письмо.
        owner_email (str): Электронная почта владельца собаки.
        views_count (int): Текущее количество просмотров записи о собаке.
    """
    send_mail(
        subject=f'{views_count} просмотров {dog_object}',  # Тема письма
        message=f'Юхуу! Уже {views_count}, просмотров записи {dog_object}',  # Сообщение письма
        from_email=settings.EMAIL_HOST_USER,  # Адрес отправителя
        recipient_list=[owner_email, ]  # Список получателей
    )
