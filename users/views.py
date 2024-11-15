import random
import string

from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm, UserForm
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'user/register_user.html'


def form_valid(self, form):
    self.object = form.save()
    send_register_email(self.object.email)
    return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'user/login_user.html'


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_profile_read_only.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'user/change_password_user.html'
    success_url = reverse_lazy('users:profile_user')


class UserLogoutView(LogoutView):
    template_name = 'user/logout_user.html'


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
