from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from dogs.models import Category, Dog
from dogs.forms import DogForm


def index(request):
    """
    View для отображения главной страницы питомника.

    :param request: Объект запроса HTTP.
    :return: Rendered HTML-страница с списком пород.
    """
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


@login_required
def categories(request):
    """
    View для отображения всех категорий собак в питомнике.

    :param request: Объект запроса HTTP.
    :return: Rendered HTML-страница с списком всех пород.
    """
    context = {
        'object_list': Category.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/categories.html', context)


@login_required
def category_dogs(request, pk):
    """
    View для отображения списка собак конкретной породы.

    :param request: Объект запроса HTTP.
    :param pk: Primary key категории.
    :return: Rendered HTML-страница с списком собак данной породы.
    """
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


class DogListView(ListView):
    model = Dog
    extra_context = {
        'title': 'Питомник - Все наши собаки',
    }
    template_name = 'dogs/dogs.html'


class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'
    success_url = reverse_lazy('dogs:list_dogs')


class DogDetailView(DetailView):
    model = Dog
    template_name = 'dogs/detail.html'


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    template_name = 'dogs/create_update.html'

    def get_success_url(self):
        return reverse('dogs:detail_dog', args=[self.kwargs.get('pk')])


@login_required
def dog_delete_view(request, pk):
    """
    View для удаления конкретной собаки из питомника.

    :param request: Объект запроса HTTP.
    :param pk: Primary key собаки.
    :return: Rendered HTML-страница для подтверждения удаления или перенаправление на список собак после успешного удаления.
    """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object,
    })
