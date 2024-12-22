from django import forms

from reviews.models import Review
from dogs.forms import StyleFormMixin


class ReviewForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования отзыва.

    Эта форма основана на модели Review и включает в себя поля для ввода заголовка, содержания и слага.

    Атрибуты:
        title (CharField): Заголовок отзыва, максимальная длина 150 символов.
        content (TextInput): Поле для ввода текста отзыва.
        slug (SlugField): Уникальный слаг для отзыва, скрытое поле с начальным значением 'temp_slug'.

    Метаданные:
        Meta: Определяет модель, к которой относится форма, и поля, которые будут включены в форму.
    """

    title = forms.CharField(max_length=150, label='Заголовок_формы')  # Заголовок отзыва
    content = forms.TextInput()  # Поле для ввода текста отзыва
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())  # Скрытое поле слага

    class Meta:
        model = Review  # Модель, к которой относится форма
        fields = ('dog', 'title', 'content', 'slug')  # Поля, включенные в форму
