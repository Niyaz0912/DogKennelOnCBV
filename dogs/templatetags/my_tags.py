"""
{% load %}
Приложение должно содержать каталог templatetags, на том же уровне, что и models.py и т.д.
Если такой каталог еще не существует, следует создать его, и не забыть про файл __init__.py,
чтобы каталог рассматривался как пакет Пайтон"""

from django import template

register = template.Library()


@register.filter()
def dogs_media(val):
    if val:
        return fr'/media/{val}'
    return '/static/INF.jpg'


@register.filter()
def user_media(val):
    if val:
        return f'/media/{val}'
    return '/static/noavatar.png'
