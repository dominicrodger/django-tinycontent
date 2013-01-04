from django import template
from django.template.base import TemplateSyntaxError
from tinycontent.models import TinyContent


register = template.Library()


class TinyContentNode(template.Node):
    def __init__(self, content_name, nodelist):
        self.content_name = content_name
        self.nodelist = nodelist

    def get_content_name(self, context):
        if self.content_name[0] != '"' and self.content_name[0] != "'":
            try:
                return context[self.content_name]
            except KeyError:
                return ''

        if self.content_name[0] == '"' and self.content_name[-1] == '"':
            return self.content_name[1:-1]

        if self.content_name[0] == "'" and self.content_name[-1] == "'":
            return self.content_name[1:-1]

        return self.content_name

    def render(self, context):
        try:
            name = self.get_content_name(context)
            obj = TinyContent.objects.get(name=name)
            return obj.content
        except TinyContent.DoesNotExist:
            return self.nodelist.render(context)


@register.tag
def tinycontent(parser, token):
    args = token.split_contents()

    if len(args) != 2:
        raise TemplateSyntaxError("'tinycontent' tag takes exactly one"
                                  " argument.")

    content_name = args[1]

    nodelist = parser.parse(('endtinycontent',))
    parser.delete_first_token()
    return TinyContentNode(content_name, nodelist)


@register.simple_tag
def tinycontent_simple(name):
    try:
        obj = TinyContent.objects.get(name=name)
        return obj.content
    except TinyContent.DoesNotExist:
        return ''
