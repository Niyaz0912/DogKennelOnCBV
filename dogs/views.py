from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm  # DogAdminForm
from dogs.services import send_views_mail
from users.models import UserRoles


def index(request):
    """
    Главная страница питомника.

    Отображает три категории собак и заголовок страницы.

    Args:
        request: HTTP запрос.

    Returns:
        HttpResponse: Рендеринг главной страницы с контекстом.
    """
    context = {
        'object_list': Category.objects.all()[:3],  # Получение первых трех категорий
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategorySearchListView(LoginRequiredMixin, ListView):
    """
    Представление для поиска категорий собак.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель Category.
        template_name: Шаблон для отображения результатов поиска.
        extra_context: Дополнительный контекст для шаблона.
    """
    model = Category
    template_name = 'dogs/categories.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        """
        Получает список категорий на основе поискового запроса.

        Returns:
            QuerySet: Список категорий, соответствующих запросу.
        """
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query),  # Фильтрация по имени категории
        )
        return object_list


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения всех категорий собак.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель Category.
        extra_context: Дополнительный контекст для шаблона.
        template_name: Шаблон для отображения списка категорий.
    """
    model = Category
    extra_context = {
        'title': 'Питомник все наши породы'
    }
    template_name = 'dogs/categories.html'


@login_required
def category_dogs(request, pk):
    """
    Представление для отображения списка собак в определенной категории.

    Args:
        request: HTTP запрос.
        pk (int): ID категории.

    Returns:
        HttpResponse: Рендеринг страницы со списком собак в категории.
    """
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),  # Получение всех собак в категории
        'title': f'Собаки породы {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка всех активных собак.

    Ограничивает доступ только для авторизованных пользователей и поддерживает пагинацию.

    Атрибуты:
        model: Модель Dog.
        paginate_by: Количество собак на странице.
        extra_context: Дополнительный контекст для шаблона.
        template_name: Шаблон для отображения списка собак.
        login_url: URL для перенаправления неавторизованных пользователей.

    Returns:
        QuerySet: Список активных собак.
    """
    model = Dog
    paginate_by = 3
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'
    login_url = '/user/'

    def get_queryset(self):
        """
        Получает список активных собак.

        Returns:
            QuerySet: Список активных собак.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)  # Фильтрация по статусу активности
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка неактивных собак.

    Ограничивает доступ только для авторизованных пользователей.
    Доступ к этому представлению зависит от роли пользователя.

    Атрибуты:
        model: Модель Dog.
        extra_context: Дополнительный контекст для шаблона.
        template_name: Шаблон для отображения списка неактивных собак.

    Returns:
        QuerySet: Список неактивных собак в зависимости от роли пользователя.
    """
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        """
        Получает список неактивных собак в зависимости от роли пользователя.

        Returns:
            QuerySet: Список неактивных собак.
        """
        queryset = super().get_queryset()

        # Фильтрация по роли пользователя
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)  # Все неактивные собаки для модераторов и администраторов

        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)  # Неактивные собаки только владельца

        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    """
    Представление для поиска собак по имени.

    Ограничивает доступ только для авторизованных пользователей.

    Атрибуты:
        model: Модель Dog.
        template_name: Шаблон для отображения результатов поиска.

     Returns:
         QuerySet: Список активных собак соответствующих запросу.
     """

    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса',
    }

    def get_queryset(self):
        """
        Получает список активных собак на основе поискового запроса.

        Returns:
            QuerySet: Список активных собак, соответствующих запросу по имени.
        """
        query = self.request.GET.get('q')
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания новой собаки.

    Ограничивает доступ только для авторизованных пользователей.
    Пользователь должен иметь роль USER для создания новой собаки.

    Атрибуты:
        model: Модель Dog.
        form_class: Форма для создания собаки (DogForm).
        template_name: Шаблон для создания/обновления собаки.
        success_url: URL перенаправления после успешного создания собаки.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу списка собак после успешного создания.
    """

    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        """
        Обрабатывает валидную форму и сохраняет собаку с текущим пользователем как владельцем.

        Args:
            form (DogForm): Валидная форма создания собаки.

        Returns:
            HttpResponseRedirect: Перенаправление на страницу списка собак после успешного создания.
        """
        if self.request.user.role != UserRoles.USER:
            return PermissionDenied()  # Запрет доступа если роль пользователя не USER

        self.object = form.save()
        self.object.owner = self.request.user  # Установка владельца как текущего пользователя
        self.object.save()

        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей собаки.

    Ограничивает доступ только для авторизованных пользователей.
    Увеличивает количество просмотров и отправляет уведомление владельцу о каждом 20-м просмотре.

    Атрибуты:
        model: Модель Dog.
        template_name: Шаблон для отображения деталей собаки.

    Returns:
        dict: Контекст с данными о собаке и заголовком страницы.
    """

    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            dict: Обновленный контекст с данными о собаке и заголовком страницы.
        """
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data['title'] = f'{object.name} {object.category}'  # Заголовок страницы

        dog_object_increase = get_object_or_404(Dog, pk=object.pk)  # Получение объекта собаки по ID

        if object.owner != self.request.user:
            dog_object_increase.views_count()  # Увеличение счетчика просмотров

            if object.owner:
                object_owner_email = object.owner.email  # Получение email владельца

                if dog_object_increase.views % 20 == 0 and dog_object_increase.views != 0:
                    send_views_mail(dog_object_increase.name, object_owner_email,
                                    dog_object_increase.views)  # Отправка уведомления

        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления информации о собаке.

    Ограничивает доступ только для авторизованных пользователей.
    Пользователь должен быть владельцем собаки или администратором.

    Атрибуты:
        model: Модель Dog.
        form_class: Форма обновления собаки (DogForm).
        template_name: Шаблон для создания/обновления собаки.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу деталей собаки после успешного обновления.
    """

    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        """Возвращает URL перенаправления после успешного обновления."""
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        """Получает объект собаки и проверяет права доступа."""

        self.object = super().get_object(queryset)

        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()  # Запрет доступа если пользователь не владелец или администратор

        return self.object

    # def get_form_class(self):
    #     dog_forms = {
    #         'admin': DogAdminForm,
    #         'moderator': DogForm,
    #         'user': DogForm,
    #     }
    #     user_role = self.request.user.role
    #     dog_forms_class = dog_forms[user_role]
    #     return dog_forms_class


    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст шаблона."""

        context_data = super().get_context_data(**kwargs)

        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)  # Создание формы набора родителей

        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)  # Обработка POST-запроса
        else:
            formset = ParentFormset(instance=self.object)  # Обработка GET-запроса

        context_data['formset'] = formset  # Добавление формы набора в контекст

        return context_data

    def form_valid(self, form):
        """Обрабатывает валидную форму и сохраняет обновленную информацию о собаке."""

        context_data = self.get_context_data()

        formset = context_data['formset']

        self.object = form.save()  # Сохранение формы

        if formset.is_valid():
            formset.instance = self.object  # Привязка формы набора к объекту собаки
            formset.save()  # Сохранение формы набора родителей

        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления собаки.

    Ограничивает доступ только для пользователей с соответствующими правами.

    Атрибуты:
       model: Модель Dog.
       template_name: Шаблон подтверждения удаления.
       success_url: URL перенаправления после успешного удаления.
       permission_required: Необходимые права доступа.

       Returns:
           HttpResponseRedirect: Перенаправление на страницу списка собак после успешного удаления.
       """

    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = 'dogs.delete_dog'


def dog_toggle_activity(request, pk):
    """
    Переключает статус активности собаки (активна/неактивна).

    Args:
       request (HttpRequest): HTTP запрос от клиента.
       pk (int): ID собаки.

    Returns:
       HttpResponseRedirect: Перенаправление на страницу списка собак после изменения статуса активности.
    """

    dog_item = get_object_or_404(Dog, pk=pk)  # Получение объекта собаки по ID

    dog_item.is_active = not dog_item.is_active  # Переключение статуса активности

    dog_item.save()  # Сохранение изменений

    return redirect(reverse('dogs:list_dogs'))  # Перенаправление на страницу списка собак

