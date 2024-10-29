from django.urls import path
from dogs.views import index, categories, category_dogs, dogs_list_view, dog_create_view, dog_detail_view, \
    dog_update_view, dog_delete_view
from dogs.apps import DogsConfig

app_name = DogsConfig.name
# URL-конфигурация для приложения 'dogs'.
# Эти URL-шаблоны определяют маршруты для различных представлений приложения.

urlpatterns = [
    path('', index, name='index'),  # URL для отображения главной страницы питомника.
    path('categories/', categories, name='categories'),  # URL для отображения списка всех пород собак.
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'),  # URL для отображения пород по порядку pk.
    path('dogs/', dogs_list_view, name='list_dogs'),  # URL для отображения всех собак питомника.
    path('dogs/create/', dog_create_view, name='create_dog'),  # URL для создания новой собаки.
    path('dogs/detail/<int:pk>/', dog_detail_view, name='detail_dog'),  # URL для отображения детальной информации о конкретной собаке.
    path('dogs/update/<int:pk>/', dog_update_view, name='update_dog'),  # URL для обновления информации о конкретной собаке.
    path('dogs/delete/<int:pk>/', dog_delete_view, name='delete_dog'),  # URL для удаления собаки.
]
