from django.urls import path

from users.apps import UsersConfig
from users.views import user_generate_new_password, UserRegisterView, UserLoginView, UserProfileView, \
    UserUpdateView, UserPasswordChangeView, UserLogoutView, UserListView, UserViewProfileView

# Устанавливаем имя пространства имен для маршрутов приложения 'users'
app_name = UsersConfig.name

urlpatterns = [
    # Работа с аккаунтом
    path('', UserLoginView.as_view(), name='login_user'),  # Страница входа пользователя
    path('logout/', UserLogoutView.as_view(), name='logout_user'),  # Выход пользователя
    path('register/', UserRegisterView.as_view(), name='register_user'),  # Регистрация нового пользователя
    path('profile/', UserProfileView.as_view(), name='profile_user'),  # Профиль текущего пользователя
    path('update/', UserUpdateView.as_view(), name='update_user'),  # Обновление данных пользователя
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password_user'),
    # Смена пароля пользователя
    path('profile/genpassword/', user_generate_new_password, name='user_generate_new_password'),
    # Генерация нового пароля

    # Просмотр других пользователей
    path('all_users/', UserListView.as_view(), name='users_list'),  # Список всех пользователей
    path('profile/<int:pk>/', UserViewProfileView.as_view(), name="profile_user_view"),
    # Просмотр профиля другого пользователя по ID
]
