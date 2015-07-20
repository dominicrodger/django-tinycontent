from django import template
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
            obj = TinyContent.objects.get(name=name)
            return render_to_string('tinycontent/tinycontent.html',
                                    {'obj': obj},
                                    context)
        except TinyContent.DoesNotExist:
            rval = self.nodelist.render(context)
            rval += render_to_string('tinycontent/tinycontent_add.html',
                                     {'name': name},
                                     context)
            return rval


@register.tag
def tinycontent(parser, token):
    args = [parser.compile_filter(x) for x in token.split_contents()[1:]]
    nodelist = parser.parse(('endtinycontent',))
    parser.delete_first_token()
    return TinyContentNode(args, nodelist)


@register.simple_tag(takes_context=True)
def tinycontent_simple(context, *args):
    content_name = ':'.join(map(unicode, args))
    try:
        obj = TinyContent.objects.get(name=content_name)
        return render_to_string('tinycontent/tinycontent.html',
                                {'obj': obj},
                                context)
    except TinyContent.DoesNotExist:
        return render_to_string('tinycontent/tinycontent_add.html',
                                {'name': content_name},
                                context)
