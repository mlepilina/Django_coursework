from django import template

register = template.Library()


@register.simple_tag
def media_path(format_string):
    if format_string:
        return f'/media/{format_string}'
    return 'none'