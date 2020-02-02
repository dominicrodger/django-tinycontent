from django import template
from django.template.base import TemplateSyntaxError
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from tinycontent.models import TinyContent


register = template.Library()


class TinyContentNode(template.Node):
    def __init__(self, args, nodelist):
        self.args = args
        self.nodelist = nodelist

    def get_name(self, context):
        return ':'.join(x.resolve(context) for x in self.args)

    def render(self, context):
        try:
            name = self.get_name(context)
            obj = TinyContent.get_content_by_name(name)
            context.update(
                {
                    'obj': obj
                }
            )
            return render_to_string('tinycontent/tinycontent.html',
                                    context.flatten())
        except TinyContent.DoesNotExist:
            rval = self.nodelist.render(context)
            context.update(
                {
                    'name': name
                }
            )
            rval += render_to_string('tinycontent/tinycontent_add.html',
                                     context.flatten())
            return rval


@register.tag
def tinycontent(parser, token):
    parts = token.split_contents()[1:]

    if not parts:
        raise TemplateSyntaxError("'tinycontent' tag takes arguments.")

    args = [parser.compile_filter(x) for x in parts]
    nodelist = parser.parse(('endtinycontent',))
    parser.delete_first_token()
    return TinyContentNode(args, nodelist)


@register.simple_tag(takes_context=True)
def tinycontent_simple(context, *args):
    if not args:
        raise TemplateSyntaxError("'tinycontent' tag takes arguments.")

    content_name = ':'.join(map(force_str, args))
    try:
        obj = TinyContent.get_content_by_name(content_name)
        context.update(
            {
                'obj': obj
            }
        )
        return render_to_string('tinycontent/tinycontent.html',
                                context.flatten())
    except TinyContent.DoesNotExist:
        context.update(
            {
                'name': content_name
            }
        )
        return render_to_string('tinycontent/tinycontent_add.html',
                                context.flatten())
