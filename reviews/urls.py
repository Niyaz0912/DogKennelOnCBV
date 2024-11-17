from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import DogReviewListView, DeactivatedDogReviewListView

app_name = ReviewsConfig.name

urlpatterns = [
    path('<int:pk>/reviews/', DogReviewListView.as_view, name='reviews_list'),
    path('<int:pk>/reviews/deactivate/', DeactivatedDogReviewListView.as_view(), name='deactivated_reviews_list_dogs'),
    ]