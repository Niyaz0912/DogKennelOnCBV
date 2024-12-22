from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Review.

    Этот класс настраивает отображение и поведение модели Review в административной панели Django.

    Атрибуты:
        list_display (tuple): Поля, которые будут отображаться в списке объектов.
        ordering (tuple): Поля, по которым будет производиться сортировка объектов в списке.
        list_filter (tuple): Поля, по которым можно фильтровать объекты в списке.
    """

    list_display = ('title', 'dog', 'autor', 'created', 'sign_of_review',)  # Поля для отображения в списке
    ordering = ('created',)  # Сортировка по дате создания
    list_filter = ('dog', 'autor',)  # Фильтры по собаке и автору отзыва

