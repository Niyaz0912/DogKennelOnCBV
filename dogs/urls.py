from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from dogs.views import index, category_dogs, DogListView, DogCreateView, \
    DogDetailView, DogUpdateView, DogDeleteView, CategoryListView
from dogs.apps import DogsConfig

app_name = DogsConfig.name

urlpatterns = [
    path('', cache_page(60)(index), name='index'),  # URL для отображения главной страницы питомника.
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories'),  # URL для отображения списка всех пород собак.
    path('categories/<int:pk>/dogs/', category_dogs, name='category_dogs'),  # URL для отображения пород по порядку pk.
    path('dogs/', DogListView.as_view(), name='list_dogs'),  # URL для отображения всех собак питомника.
    path('dogs/create/', DogCreateView.as_view(), name='create_dog'),  # URL для создания новой собаки.
    path('dogs/detail/<int:pk>/', DogDetailView.as_view(), name='detail_dog'),  # URL для отображения детальной информации о конкретной собаке.
    path('dogs/update/<int:pk>/', never_cache(DogUpdateView.as_view()), name='update_dog'),  # URL для обновления информации о конкретной собаке.
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='delete_dog'),  # URL для удаления собаки.
]
