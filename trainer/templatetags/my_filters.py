from django import template

register = template.Library()

@register.filter()
def limit(min):
    return range(min)