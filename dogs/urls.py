from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from dogs.views import index, category_dogs, DogListView, DogCreateView, DogDetailView, DogUpdateView, DogDeleteView, \
    CategoryListView, DogDeactivateListView, DogSearchListView, dog_toggle_activity, CategorySearchListView
from dogs.apps import DogsConfig

# Устанавливаем имя пространства имен для маршрутов приложения 'dogs'
app_name = DogsConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),  # Главная страница с кешированием на 60 секунд
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),  # Список категорий с
    # кешированием
    path('categories/search', CategorySearchListView.as_view(), name='search_categories'),  # Поиск категорий
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'),  # Список собак по категории
    path('dogs/', DogListView.as_view(), name='list_dogs'),  # Список всех собак
    path('dogs/deactivate/', DogDeactivateListView.as_view(), name='deactivated_list_dogs'),  # Список неактивных собак
    path('dogs/search/', DogSearchListView.as_view(), name='search_dogs'),  # Поиск собак
    path('dogs/create/', DogCreateView.as_view(), name='create_dog'),  # Создание новой собаки
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='detail_dog'),  # Детали собаки по ID
    path('dogs/toggle/<int:pk>', dog_toggle_activity, name='toggle_activity_dog'),  # Переключение активности собаки
    # по ID
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='update_dog'),  # Обновление информации о
    # собаке без кеширования
    path('dogs/delete/<int:pk>', DogDeleteView.as_view(), name='delete_dog'),  # Удаление собаки по ID
]
