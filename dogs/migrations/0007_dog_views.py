# Generated by Django 5.0.9 on 2024-11-14 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0006_dog_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='views',
            field=models.IntegerField(default=0, verbose_name='просмотры'),
        ),
    ]