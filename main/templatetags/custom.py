from django import template

register = template.Library()

@register.filter
def multiply(value, arg=1):
    try:
        value = round(value * arg)
    except (TypeError, ValueError):
        pass
    return value
