from django import template
from tinycontent.models import TinyContent


register = template.Library()


@register.simple_tag
def tinycontent(name):
    try:
        obj = TinyContent.objects.get(name=name)
        return obj.content
    except TinyContent.DoesNotExist:
        return ''
