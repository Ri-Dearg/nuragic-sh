from django import template

register = template.Library()


@register.filter(name='extension')
def extension(value):
    """
        Returns the value turned into a list.
    """
    return value.rsplit('.')[-1]
