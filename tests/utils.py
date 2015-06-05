from django.contrib.auth.context_processors import PermWrapper
from django.template import Context, Template


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context()
    return t.render(c).strip()


def render_template_with_context(input, context):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context(context)
    return t.render(c).strip()


def render_for_test_user(t, user):
    ctx = {'user': user, 'perms': PermWrapper(user), }
    return render_template_with_context(t, ctx)


def toupper(content):
    return content.upper()


def truncate_ten(content):
    return content[:10]


def reverse(content):
    return content[::-1]
