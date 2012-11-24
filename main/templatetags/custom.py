from django import template
import math

register = template.Library()

@register.filter
def multiply(value, arg=1):
    try:
        value = math.ceil(value * arg)
    except (TypeError, ValueError):
        pass
        
    
    return value
