from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'pk', 'is_active')
    list_filter = ('last_name', 'is_active')  # Добавлено поле is_active для фильтрации
    search_fields = ('email', 'last_name', 'first_name')  # Добавлена возможность поиска
    ordering = ('last_name', 'first_name')  # Установлена сортировка по умолчанию
