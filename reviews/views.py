from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import UserRoles
from reviews.forms import ReviewForm
from reviews.utils import slug_generator


class ReviewListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех активных отзывов.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель Review.
        extra_context: Дополнительный контекст для шаблона.
        template_name: Шаблон для отображения списка отзывов.

    Returns:
        QuerySet: Список активных отзывов.
    """
    model = Review
    extra_context = {
        'title': 'Все отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        """
        Получает список активных отзывов.

        Returns:
            QuerySet: Список отзывов с активным статусом.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)  # Фильтрация по статусу активности
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка неактивных отзывов.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель Review.
        extra_context: Дополнительный контекст для шаблона.
        template_name: Шаблон для отображения списка неактивных отзывов.

    Returns:
        QuerySet: Список неактивных отзывов.
    """
    model = Review
    extra_context = {
        'title': 'Неактивные отзывы'
    }
    template_name = 'reviews/reviews_list.html'

    def get_queryset(self):
        """
        Получает список неактивных отзывов.

        Returns:
            QuerySet: Список отзывов с неактивным статусом.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False)  # Фильтрация по статусу активности
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового отзыва.

    Ограничивает доступ только для авторизованных пользователей.
    Проверяет роль пользователя перед сохранением отзыва.

    Атрибуты:
        model: Модель Review.
        form_class: Форма для создания отзыва (ReviewForm).
        template_name: Шаблон для создания/обновления отзыва.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу деталей отзыва после успешного создания.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет новый отзыв.

        Args:
            form (ReviewForm): Валидная форма создания отзыва.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу деталей отзыва после успешного создания.
        """
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden()  # Запрет доступа если роль пользователя не USER или ADMIN

        self.object = form.save()  # Сохранение формы

        if self.object.slug == 'temp_slug':
            self.object.slug = slug_generator()  # Генерация уникального слага если он временный

        self.object.autor = self.request.user  # Установка текущего пользователя как автора отзыва
        self.object.save()  # Сохранение объекта отзыва

        return super().form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей отзыва.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
         model: Модель Review.
         template_name: Шаблон для отображения деталей отзыва.

     Returns:
         HttpResponse: Рендеринг страницы с деталями отзыва.
     """

    model = Review
    template_name = 'reviews/review_detail.html'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления существующего отзыва.

    Ограничивает доступ только для авторизованных пользователей.
    Проверяет права доступа перед обновлением отзыва.

    Атрибуты:
         model: Модель Review.
         form_class: Форма обновления отзыва (ReviewForm).
         template_name: Шаблон для создания/обновления отзыва.

     Returns:
         HttpResponseRedirect: Перенаправление на страницу деталей отзыва после успешного обновления.
     """

    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create_update.html'

    def get_success_url(self):
        """Возвращает URL перенаправления после успешного обновления."""
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        """Получает объект отзыва и проверяет права доступа."""
        self.object = super().get_object(queryset)

        if self.object.autor != self.request.user and self.request.user not in [UserRoles.ADMIN,
                                                                                UserRoles.MODERATOR]:
            raise PermissionDenied()  # Запрет доступа если пользователь не владелец или администратор

        return self.object


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления отзыва.

    Ограничивает доступ только для пользователей с соответствующими правами.

    Атрибуты:
         model: Модель Review.
         template_name: Шаблон подтверждения удаления.
         permission_required: Необходимые права доступа.

     Returns:
         HttpResponseRedirect: Перенаправление на страницу списка отзывов после успешного удаления.
     """

    model = Review
    template_name = 'reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        """Возвращает URL перенаправления после успешного удаления."""
        return reverse('reviews:list_reviews')


def review_toggle_activity(request, slug):
    """
    Переключает статус активности отзыва (активный/неактивный).

    Args:
        request (HttpRequest): HTTP запрос от клиента.
        slug (str): Уникальный слаг отзыва.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу со списком активных или неактивных отзывов в зависимости от статуса.
    """

    review_item = get_object_or_404(Review, slug=slug)  # Получение объекта отзыва по слагу

    if review_item.sign_of_review:
        review_item.sign_of_review = False  # Установка статуса неактивным
        review_item.save()
        return redirect(reverse('reviews:deactivated_reviews'))  # Перенаправление на страницу неактивных отзывов
    else:
        review_item.sign_of_review = True  # Установка статуса активным
        review_item.save()
        return redirect(reverse('reviews:list_reviews'))  # Перенаправление на страницу активных отзывов

