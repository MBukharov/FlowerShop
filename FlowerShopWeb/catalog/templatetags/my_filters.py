from django import template

register = template.Library()


@register.filter
def slice_from_eighth(value):
    return value[8:]