# Generated by Django 5.0.9 on 2024-11-17 15:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0007_dog_views'),
        ('reviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=25, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('sign_of_review', models.BooleanField(default=True, verbose_name='активный')),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='dogs.dog', verbose_name='Собака')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.DeleteModel(
            name='Reviews',
        ),
    ]
