from django.db import models
from django.conf import settings

from users.models import NULLABLE


class Category(models.Model):
    """
    Модель для категории собак (породы).

    Атрибуты:
    - name: Название породы (CharField, макс. 100 символов).
    - description: Описание породы (CharField, макс. 1000 символов).

    Методы:
    - __str__(): Возвращает строковое представление названия породы.

    Метаданные:
    - verbose_name: Человекочитаемое имя модели в единственном числе.
    - verbose_name_plural: Человекочитаемое имя модели во множественном числе.
    """
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='descriptions')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """
    Модель для собаки.

    Атрибуты:
    - name: Имя собаки (CharField, макс. 250 символов).
    - category: Связь с моделью Category (ForeignKey), указывающая на породу собаки.
    - photo: Фото собаки (ImageField), загружается в папку 'dogs/'.
    - birth_date: Дата рождения собаки (DateField).
    - is_active: Статус активности собаки (BooleanField), по умолчанию True.
    - owner: Владелец собаки (ForeignKey), указывающий на пользователя.
    - views: Количество просмотров профиля собаки (IntegerField), по умолчанию 0.

    Методы:
    - __str__(): Возвращает строковое представление имени собаки и её породы.
    - views_count(): Увеличивает количество просмотров и сохраняет объект.

    Метаданные:
    - verbose_name: Человекочитаемое имя модели в единственном числе.
    - verbose_name_plural: Человекочитаемое имя модели во множественном числе.
    """
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    photo = models.ImageField(upload_to='dogs/', **NULLABLE, verbose_name='image')
    birth_date = models.DateField(**NULLABLE, verbose_name='birth_date')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name="владелец")
    views = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'dog'  # понятное человеку имя модели
        verbose_name_plural = 'dogs'  # понятное человеку имя множественное число

    def views_count(self):
        """Увеличивает количество просмотров на 1 и сохраняет объект."""
        self.views += 1
        self.save()


class Parent(models.Model):
    """
    Модель для родителя собаки.

    Атрибуты:
    - dog: Связь с моделью Dog (ForeignKey), указывающая на собаку-ребенка.
    - name: Имя родителя (CharField, макс. 250 символов).
    - category: Связь с моделью Category (ForeignKey), указывающая на породу родителя.
    - birth_date: Дата рождения родителя (DateField).

    Методы:
    - __str__(): Возвращает строковое представление имени родителя и его породы.

    Метаданные:
    - verbose_name: Человекочитаемое имя модели в единственном числе.
    - verbose_name_plural: Человекочитаемое имя модели во множественном числе.
    """
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    birth_date = models.DateField(**NULLABLE, verbose_name='birth_date')

    def __str__(self):
        return f'{self.name}({self.category})'

    class Meta:
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
