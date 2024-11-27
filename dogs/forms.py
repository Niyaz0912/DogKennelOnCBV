import datetime

from django import forms
from dogs.models import Dog, Parent
from users.forms import StyleFormMixin


# Форма для модели Dog, наследующая функциональность от StyleFormMixin
class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        # Указываем модель, для которой создается форма
        model = Dog
        # Исключаем поля owner, is_active и views из формы
        exclude = ('owner', 'is_active', 'views')

    # Метод для валидации даты рождения собаки
    def clean_birth_date(self):
        # Проверяем, есть ли дата рождения в очищенных данных
        if self.cleaned_data['birth_date']:
            cleaned_data = self.cleaned_data['birth_date']
            now_year = datetime.datetime.now().year  # Получаем текущий год
            # Проверяем, чтобы собака была моложе 100 лет
            if now_year - cleaned_data.year > 100:
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cleaned_data  # Возвращаем очищенные данные, если валидация прошла успешно
        return  # Возвращаем None, если дата рождения не указана


# Форма для администрирования модели Dog, также наследует от StyleFormMixin
class DogAdminForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        # Указываем все поля модели для формы
        fields = '__all__'

    @staticmethod
    def clean_birth_date():
        # Вызываем метод валидации даты рождения из DogForm
        DogForm.clean_birth_date()


# Форма для модели Parent, наследующая функциональность от StyleFormMixin
class ParentForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Parent
        # Указываем все поля модели для формы
        fields = '__all__'
