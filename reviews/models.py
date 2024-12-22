from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    """
    Модель для отзыва о собаке.

    Эта модель хранит информацию о отзыве, включая заголовок, содержание, дату создания,
    активность отзыва, автора и связанную собаку.

    Атрибуты:
        title (CharField): Заголовок отзыва, максимальная длина 150 символов.
        slug (SlugField): Уникальный слаг для отзыва, используется в URL.
        content (TextField): Содержимое отзыва.
        created (DateTimeField): Дата и время создания отзыва, автоматически устанавливается при добавлении.
        sign_of_review (BooleanField): Статус активности отзыва (по умолчанию True).
        autor (ForeignKey): Связь с пользователем, который написал отзыв.
        dog (ForeignKey): Связь с моделью Dog, указывающая на собаку, к которой относится отзыв.

    Методы:
        __str__(): Возвращает строковое представление отзыва по заголовку.
        get_absolute_url(): Возвращает URL для просмотра деталей отзыва.

    Метаданные:
        verbose_name: Человекочитаемое имя модели в единственном числе.
        verbose_name_plural: Человекочитаемое имя модели во множественном числе.
    """

    title = models.CharField(max_length=150, verbose_name='Заголовок')  # Заголовок отзыва
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')  # Уникальный слаг
    content = models.TextField(verbose_name='Содержимое')  # Содержимое отзыва
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)  # Дата создания
    sign_of_review = models.BooleanField(default=True, verbose_name='активный')  # Статус активности
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Автор')  # Автор отзыва
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='dogs', verbose_name='Собака')  # Связанная собака

    def __str__(self):
        """Возвращает строковое представление заголовка отзыва."""
        return f'{self.title}'

    def get_absolute_url(self):
        """Возвращает URL для просмотра деталей отзыва."""
        return reverse('reviews:detail_review', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'review'  # Человекочитаемое имя модели в единственном числе
        verbose_name_plural = 'reviews'  # Человекочитаемое имя модели во множественном числе

