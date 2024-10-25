"""
{% load %}
Приложение должно содержать каталог templatetags, на том же уровне, что и models.py и т.д.
Если такой каталог еще не существует, следует создать его, и не забыть про файл __init__.py,
чтобы каталог рассматривался как пакет Пайтон"""


from django import template

register = template.Library()


@register.filter()
def mymedia(val):
    if val:
        return fr'/media/{val}'
    return '/static/INF.jpg'
