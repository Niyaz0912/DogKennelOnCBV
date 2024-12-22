import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Эта форма позволяет пользователю создать новый аккаунт и отправляет
    электронное письмо с подтверждением регистрации.

    Атрибуты:
        model: Модель пользователя (User).
        form_class: Форма регистрации (UserRegisterForm).
        success_url: URL для перенаправления после успешной регистрации.
        template_name: Шаблон для отображения формы регистрации.
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')  # URL для перенаправления после успешной регистрации
    template_name = 'user/register_user.html'

    def form_valid(self, form):
        """
        Обрабатывает валидную форму регистрации.

        Args:
            form (UserRegisterForm): Валидная форма регистрации.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу входа после успешной регистрации.
        """
        self.object = form.save()  # Сохранение нового пользователя
        send_register_email(self.object.email)  # Отправка письма с подтверждением регистрации
        return super().form_valid(form)  # Перенаправление на success_url


class UserLoginView(LoginView):
    """
    Представление для входа пользователя.

    Позволяет пользователю ввести свои учетные данные для входа в систему.

    Атрибуты:
        template_name: Шаблон для отображения формы входа.
        form_class: Форма входа (UserLoginForm).
    """
    template_name = 'user/login_user.html'  # Шаблон для формы входа
    form_class = UserLoginForm  # Форма для аутентификации


class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    Представление для просмотра и редактирования профиля текущего пользователя.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель пользователя (User).
        form_class: Форма профиля (UserForm).
        template_name: Шаблон для отображения профиля.

    Returns:
         HttpResponse: Рендеринг страницы профиля пользователя.
     """

    model = User
    form_class = UserForm
    template_name = 'user/user_profile_read_only.html'

    def get_object(self, queryset=None):
        """Возвращает текущего авторизованного пользователя."""
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления данных текущего пользователя.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель пользователя (User).
        form_class: Форма обновления пользователя (UserUpdateForm).
        template_name: Шаблон для формы обновления.
        success_url: URL для перенаправления после успешного обновления.

     Returns:
         HttpResponseRedirect: Перенаправление на страницу профиля после успешного обновления.
     """

    model = User
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users:profile_user')  # URL для перенаправления после успешного обновления

    def get_object(self, queryset=None):
        """Возвращает текущего авторизованного пользователя."""
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Представление для изменения пароля текущего пользователя.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
         form_class: Форма изменения пароля (UserPasswordChangeForm).
         template_name: Шаблон для формы изменения пароля.
         success_url: URL для перенаправления после успешной смены пароля.

     Returns:
         HttpResponseRedirect: Перенаправление на страницу профиля после успешной смены пароля.
     """

    form_class = UserPasswordChangeForm
    template_name = 'user/change_password_user.html'  # Шаблон для изменения пароля
    success_url = reverse_lazy('users:profile_user')  # URL для перенаправления после смены пароля


class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.

    Атрибуты:
         template_name: Шаблон для отображения страницы выхода.

     Returns:
         HttpResponse: Рендеринг страницы выхода.
     """

    template_name = 'user/logout_user.html'  # Шаблон для страницы выхода


class UserListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех активных пользователей.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
         model: Модель пользователя (User).
         extra_context: Дополнительный контекст с заголовком страницы.
         template_name: Шаблон для отображения списка пользователей.

     Returns:
         QuerySet: Список активных пользователей.
     """

    model = User
    extra_context = {
        'title': 'Питомник все наши заводчики'  # Заголовок страницы
    }
    template_name = 'user/users.html'

    def get_queryset(self):
        """Получает список активных пользователей."""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)  # Фильтрация по статусу активности
        return queryset


class UserViewProfileView(DetailView):
    """
    Представление для просмотра профиля другого пользователя.

    Атрибуты:
         model: Модель пользователя (User).
         template_name: Шаблон для отображения профиля пользователя.

     Returns:
         HttpResponse: Рендеринг страницы профиля другого пользователя.
     """

    model = User
    template_name = 'user/user_view_profile.html'  # Шаблон для просмотра профиля


@login_required
def user_generate_new_password(request):
    """
    Генерирует новый случайный пароль и отправляет его пользователю по электронной почте.

    Args:
        request (HttpRequest): HTTP запрос от клиента.

    Returns:
        HttpResponseRedirect: Перенаправление на главную страницу после генерации нового пароля.
    """

    new_password = ''.join(
        random.sample((string.ascii_letters + string.digits), 12))  # Генерация нового пароля длиной 12 символов
    request.user.set_password(new_password)  # Установка нового пароля пользователю
    request.user.save()  # Сохранение изменений в базе данных
    send_new_password(request.user.email, new_password)  # Отправка нового пароля на электронную почту пользователя
    return redirect(reverse('dogs:index'))  # Перенаправление на главную страницу питомника
