from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from dogs.models import Category, Dog
from dogs.forms import DogForm


def index(request):
    context = {
        'object_list': Category.objects.all()[:],
        'title': 'Питомник - Главная'
    }
    return render(request, 'dogs/index.html', context)


def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Питомник - Все наши породы'
    }
    return render(request, 'dogs/categories.html', context)


def category_dogs(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Dog.objects.filter(category_id=pk),
        'title': f'Собаки породы {category_item.name}',
        'category_pk': category_item.pk,
    }
    return render(request, 'dogs/dogs.html', context)


def dogs_list_view(request):
    context = {
        'object_list': Dog.objects.all(),
        'title': 'Питомник - Все наши собаки',
    }
    return render(request, 'dogs/dog.html', context)


def dog_create_view(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/create.html', {'form': DogForm()})


def dog_detail_view(request, pk):
    context = {
        'object': Dog.objects.get(pk=pk),
        'title': 'Вы выбрали данного питомца'
    }
    return render(request, 'dogs/detail.html', context)


def dog_update_view(request, pk):
    # dog_object = Dog.objects.get(pk=pk)
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog_object)
        if form.is_valid():
            dog_object = form.save()
            dog_object.save()
            return HttpResponseRedirect(reverse('dogs:detail_dog', args={pk: pk}))
    return render(request, 'dogs/update.html', {
        'object': dog_object,
        'form': DogForm(instance=dog_object)
    })


def dog_delete_view(request, pk):
    dog_object = get_object_or_404(Dog, pk=pk)
    if request.method == 'POST':
        dog_object.delete()
        return HttpResponseRedirect(reverse('dogs:list_dogs'))
    return render(request, 'dogs/delete.html', {
        'object': dog_object,
    })
