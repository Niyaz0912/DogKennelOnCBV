from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import UserRoles
from reviews.forms import ReviewForm


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Невктивные отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def get_success_url(self):
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.autor != self.request.user or self.request.user not in [UserRoles.ADMIN,
                                                                               UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:list_reviews')


def review_toggle_activity(request, slug):
    review_item = get_object_or_404(Review, slug=slug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:deactivated_reviews'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:list_reviews'))
