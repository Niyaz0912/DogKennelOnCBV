from django.contrib import admin
from dogs.models import Dog, Category


# Регистрация модели Category в админке с настройками отображения
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  # Поля, которые будут отображаться в списке категорий
    list_display = ('pk', 'name')  # Упорядочивание категорий по первичному ключу
    ordering = ('pk',)


# Регистрация модели Dog в админке с настройками отображения
@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):  # Поля, которые будут отображаться в списке собак
    list_display = ('name', 'category')  # Фильтрация по категории в списке собак
    list_filter = ('category',)  # Упорядочивание собак по имени
    ordering = ('name',)
