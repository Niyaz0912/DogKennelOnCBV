from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied

from dogs.models import Category, Dog, Parent
from dogs.forms import DogForm, ParentForm  #DogAdminForm
from dogs.services import send_views_mail
from users.models import UserRoles


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


class CategorySearchListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dogs/categories.html'
    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Category.objects.filter(
            Q(name__icontains=query),
        )
        return object_list


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Питомник все наши породы'
    }
    template_name = 'dogs/categories.html'


@login_required
def category_dogs(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(LoginRequiredMixin, ListView):
    model = Dog
    paginate_by = 3
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'
    login_url = '/user/'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DogDeactivateListView(LoginRequiredMixin, ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - неактивные собаки',
    }
    template_name = 'dogs/dogs.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role in [UserRoles.MODERATOR, UserRoles.ADMIN]:
            queryset = queryset.filter(is_active=False)
        if self.request.user.role == UserRoles.USER:
            queryset = queryset.filter(is_active=False, owner=self.request.user)
        return queryset


class DogSearchListView(LoginRequiredMixin, ListView):
    model = Dog
    template_name = 'dogs/dogs.html'
    extra_context = {
        'title': 'Результаты поискового запроса',
    }

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Dog.objects.filter(
            Q(name__icontains=query), is_active=True,
        )
        return object_list


class DogCreateView(LoginRequiredMixin, CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')

    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            return PermissionDenied()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog
    template_name = 'dogs/detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object = self.get_object()
        context_data['title'] = f'{object.name} {object.category}'
        dog_object_increase = get_object_or_404(Dog, pk=object.pk)
        # if object.owner != self.request.user and self.request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
        if object.owner != self.request.user:
            dog_object_increase.views_count()
        if object.owner:
            object_owner_email = object.owner.email
            if dog_object_increase.views % 20 == 0 and dog_object_increase.views != 0:
                send_views_mail(dog_object_increase.name, object_owner_email, dog_object_increase.views)
        return context_data


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and self.request.user.role != UserRoles.ADMIN:
            raise PermissionDenied()
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
        context_data = super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class DogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Dog
    template_name = 'dogs/delete.html'
    success_url = reverse_lazy('dogs:list_dogs')
    permission_required = 'dogs.delete_dog'


def dog_toggle_activity(request, pk):
    dog_item = get_object_or_404(Dog, pk=pk)
    if dog_item.is_active:
        dog_item.is_active = False
    else:
        dog_item.is_active = True
    dog_item.save()
    return redirect(reverse('dogs:list_dogs'))
