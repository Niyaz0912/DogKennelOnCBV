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


@login_required
def dog_create_view(request):
    """
    View для создания новой собаки в питомнике.

    :param request: Объект запроса HTTP.
    :return: Rendered HTML-страница для создания новой собаки или перенаправление на список собак после успешного создания.
    """
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_object = form.save()
            dog_object.owner = request.user
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:list_dogs'))
    context = {
        'title': 'Добавление питомца',
        'form': DogForm(),
    }
    return render(request, 'dogs/create_update.html', context)


@login_required
def dog_detail_view(request, pk):
    """
    View для отображения детальной информации о конкретной собаке.

    :param request: Объект запроса HTTP.
    :param pk: Primary key собаки.
    :return: Rendered HTML-страница с детальной информацией о собаке.
    """
    context = {
        'object': Dog.objects.get(pk=pk),
        'title': 'Вы выбрали данного питомца'
    }
    return render(request, 'dogs/detail.html', context)


@login_required
def dog_update_view(request, pk):
    """
    View для обновления информации о конкретной собаке.

    :param request: Объект запроса HTTP.
    :param pk: Primary key собаки.
    :return: Rendered HTML-страница для обновления информации о собаке или перенаправление на детальную страницу собаки
    после успешного обновления.
    """
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:detail_dog', args={pk: pk}))
    context = {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    }
    return render(request, 'dogs/create_update.html', context)


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
