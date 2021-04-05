"""A filter used to split the file extension from the filename."""
from django import template

register = template.Library()


@register.filter(name='extension')
def extension(value):
    """Splits the string at the first '.' from the right."""
    return value.rsplit('.')[-1]
