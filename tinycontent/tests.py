from django.contrib.auth.models import User, Permission
from django.contrib.auth.context_processors import PermWrapper
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.base import TemplateSyntaxError
from django.test import TestCase
from django.test.utils import override_settings

from tinycontent.models import TinyContent


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context()
    return t.render(c).strip()


def render_template_with_context(input, context):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context(context)
    return t.render(c).strip()


def render_for_test_user(t):
    user = User.objects.get(username='dom')
    ctx = {'user': user, 'perms': PermWrapper(user), }
    return render_template_with_context(t, ctx)


class TinyContentTestCase(TestCase):
    def setUp(self):
        TinyContent.objects.get_or_create(name='foobar',
                                          content='This is a test.')
        TinyContent.objects.get_or_create(name='html',
                                          content='<strong>&amp;</strong>')

    def test_str(self):
        self.assertEqual("foobar",
                         str(TinyContent.objects.get(name='foobar')))

    def test_non_existent(self):
        self.assertEqual("",
                         render_template("{% tinycontent_simple 'foo' %}"))

    def test_simple_existent(self):
        self.assertEqual("This is a test.",
                         render_template("{% tinycontent_simple 'foobar' %}"))

    def test_alternate_text_if_not_found(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("I could not find it.",
                         render_template(t))

    def test_alternate_text_if_found(self):
        t = ("{% tinycontent 'foobar' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("This is a test.",
                         render_template(t))

    def test_alternate_text_if_found_double_quotes(self):
        t = ('{% tinycontent "foobar" %}'
             'I could not find it.'
             '{% endtinycontent %}')

        self.assertEqual("This is a test.",
                         render_template(t))

    def test_alternate_text_if_not_found_with_embedded_tags(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find {{ meaning }}."
             "{% endtinycontent %}")

        ctx = {'meaning': 42}

        self.assertEqual("I could not find 42.",
                         render_template_with_context(t, ctx))

    def test_allows_context_variables_as_content_names_from_simple(self):
        t = ("{% tinycontent_simple content_name %}")

        ctx = {'content_name': 'foobar'}

        self.assertEqual("This is a test.",
                         render_template_with_context(t, ctx))

    def test_allows_context_variables_as_content_names_from_complex(self):
        t = ("{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}")

        ctx = {'content_name': 'foobar'}

        self.assertEqual("This is a test.",
                         render_template_with_context(t, ctx))

    def test_allows_with_tag_as_content_names_from_simple(self):
        t = ("{% with content_name='foobar' %}"
             "{% tinycontent_simple content_name %}"
             "{% endwith %}")

        self.assertEqual("This is a test.",
                         render_template(t))

    def test_allows_with_tag_as_content_names_from_complex(self):
        t = ("{% with content_name='foobar' %}"
             "{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}"
             "{% endwith %}")

        self.assertEqual("This is a test.",
                         render_template(t))

    def test_allows_unprovided_ctx_variables_as_content_name_complex(self):
        t = ("{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}")

        self.assertEqual("Text if empty.",
                         render_template(t))

    def test_allows_unprovided_ctx_variables_as_content_name_simple(self):
        t = ("{% tinycontent_simple content_name %}")

        self.assertEqual("",
                         render_template(t))

    def test_ctx_variables_with_name_of_content_complex(self):
        t = ("{% tinycontent foobar %}"
             "Text if empty."
             "{% endtinycontent %}")

        self.assertEqual("Text if empty.",
                         render_template(t))

    def test_ctx_variables_with_name_of_content_simple(self):
        t = ("{% tinycontent_simple foobar %}")

        self.assertEqual("",
                         render_template(t))

    def test_wrong_number_of_arguments(self):
        t = ("{% tinycontent %}{% endtinycontent %}")
        self.assertRaises(TemplateSyntaxError, lambda: render_template(t))

    def test_bad_arguments(self):
        t = ("{% tinycontent 'foo %}{% endtinycontent %}")
        self.assertRaises(TemplateSyntaxError, lambda: render_template(t))

        t = ('{% tinycontent "foo %}{% endtinycontent %}')
        self.assertRaises(TemplateSyntaxError, lambda: render_template(t))

    def test_with_user(self):
        user, is_new_user = User.objects.get_or_create(username='dom')

        t = ("{% tinycontent 'foobar' %}"
             "Text if empty."
             "{% endtinycontent %}")

        self.assertEqual("This is a test.",
                         render_for_test_user(t))

        perm = Permission.objects.get(codename='change_tinycontent')
        user.user_permissions.add(perm)
        user.save()

        root_edit_url = reverse('admin:tinycontent_tinycontent_change',
                                args=[1, ])

        rendered = render_for_test_user(t)
        self.assertTrue(root_edit_url in rendered)
        self.assertTrue('Edit' in rendered)
        self.assertTrue("This is a test." in rendered)

        t = "{% tinycontent_simple 'foobar' %}"
        rendered = render_for_test_user(t)
        self.assertTrue(root_edit_url in rendered)
        self.assertTrue('Edit' in rendered)
        self.assertTrue("This is a test." in rendered)

    def test_with_user_for_nonexistent_tag(self):
        user, is_new_user = User.objects.get_or_create(username='dom')

        t = ("{% tinycontent 'notthere' %}"
             "Text if empty."
             "{% endtinycontent %}")

        self.assertEqual("Text if empty.",
                         render_for_test_user(t))

        perm = Permission.objects.get(codename='add_tinycontent')
        user.user_permissions.add(perm)
        user.save()

        root_add_url = reverse('admin:tinycontent_tinycontent_add')

        rendered = render_for_test_user(t)
        self.assertTrue('%s?name=notthere' % root_add_url in rendered)
        self.assertTrue('Add' in rendered)
        self.assertTrue("Text if empty." in rendered)

        t = "{% tinycontent_simple 'notthere' %}"
        rendered = render_for_test_user(t)
        self.assertTrue('%s?name=notthere' % root_add_url in rendered)
        self.assertTrue('Add' in rendered)

    def test_with_html_simple(self):
        self.assertEqual("<strong>&amp;</strong>",
                         render_template("{% tinycontent_simple 'html' %}"))

    def test_with_html_complex(self):
        self.assertEqual("<strong>&amp;</strong>",
                         render_template("{% tinycontent 'html' %}"
                                         "Not found."
                                         "{% endtinycontent %}"))

    @override_settings(TINYCONTENT_FILTER='tinycontent.tests.toupper')
    def test_with_custom_filter_simple(self):
        self.assertEqual("THIS IS A TEST.",
                         render_template("{% tinycontent_simple 'foobar' %}"))

    @override_settings(TINYCONTENT_FILTER='tinycontent.tests.toupper')
    def test_with_custom_filter_complex(self):
        self.assertEqual("THIS IS A TEST.",
                         render_template("{% tinycontent 'foobar' %}"
                                         "Not found."
                                         "{% endtinycontent %}"))

    @override_settings(TINYCONTENT_FILTER='tinycontent.tests.toupper')
    def test_with_custom_filter_simple_with_html(self):
        self.assertEqual("<STRONG>&AMP;</STRONG>",
                         render_template("{% tinycontent_simple 'html' %}"))

    @override_settings(TINYCONTENT_FILTER='tinycontent.tests.toupper')
    def test_with_custom_filter_complex_with_html(self):
        self.assertEqual("<STRONG>&AMP;</STRONG>",
                         render_template("{% tinycontent 'html' %}"
                                         "Not found."
                                         "{% endtinycontent %}"))

    @override_settings(TINYCONTENT_FILTER='tinycontent.tests.ohnothisisfake')
    def test_with_bad_custom_filter(self):
        with self.assertRaises(ImproperlyConfigured):
            render_template("{% tinycontent_simple 'foobar' %}")


def toupper(content):
    return content.upper()
