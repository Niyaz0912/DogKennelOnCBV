from django.http import HttpResponseRedirect

from django.shortcuts import render, reverse

from users.models import User
from users.forms import UserRegisterForm


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('dog_index'))
    return render(request, 'user/register_user.html', {'form': UserRegisterForm}, )
