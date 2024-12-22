"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls')
"""

# Импорт необходимых модулей из Django
from django.conf import settings  # Импорт настроек проекта
from django.contrib import admin  # Импорт административного интерфейса
from django.urls import path, include  # Импорт функций для работы с URL
from django.conf.urls.static import static  # Импорт для работы со статическими файлами

# Список маршрутов URL
urlpatterns = [
    path('admin/', admin.site.urls),  # URL для административного интерфейса
    path('', include('dogs.urls', namespace='dogs')),  # Включение маршрутов приложения 'dogs'
    path('users/', include('users.urls', namespace='users')),  # Включение маршрутов приложения 'users'
    path('reviews/', include('reviews.urls', namespace='reviews')),  # Включение маршрутов приложения 'reviews'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Обработка статических файлов для медиа-контента
