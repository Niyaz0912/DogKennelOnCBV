from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import ReviewListView, ReviewDeactivatedListView, ReviewCreateView, ReviewDetailView, \
    ReviewUpdateView, ReviewDeleteView, review_toggle_activity

# Устанавливаем имя пространства имен для маршрутов приложения 'reviews'
app_name = ReviewsConfig.name

urlpatterns = [
    path('', ReviewListView.as_view(), name='list_reviews'),  # Список всех отзывов
    path('deactivated/', ReviewDeactivatedListView.as_view(), name='deactivated_reviews'),  # Список неактивных отзывов
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),  # Создание нового отзыва
    path('review/detail/<slug:slug>/', ReviewDetailView.as_view(), name='detail_review'),  # Детали отзыва по слагу
    path('review/update/<slug:slug>/', ReviewUpdateView.as_view(), name='update_review'),  # Обновление отзыва по слагу
    path('review/delete/<slug:slug>/', ReviewDeleteView.as_view(), name='delete_review'),  # Удаление отзыва по слагу
    path('review/toggle/<slug:slug>/', review_toggle_activity, name='toggle_activity_review'),  # Переключение
    # активности отзыва по слагу
]
