from django.template import Context, Template
from django.template.base import TemplateSyntaxError
from tinycontent.models import TinyContent
import unittest


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context()
    return t.render(c)


def render_template_with_context(input, context):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context(context)
    return t.render(c)


class TinyContentTestCase(unittest.TestCase):
    def setUp(self):
        TinyContent.objects.get_or_create(name='foobar',
                                          content='This is a test.')

    def testUnicode(self):
        self.assertEqual("foobar",
                         unicode(TinyContent.objects.get(name='foobar')))

    def testNonExistent(self):
        self.assertEqual("",
                         render_template("{% tinycontent_simple 'foo' %}"))

    def testSimpleExistent(self):
        self.assertEqual("This is a test.",
                         render_template("{% tinycontent_simple 'foobar' %}"))

    def testAlternateTextIfNotFound(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("I could not find it.",
                         render_template(t))

    def testAlternateTextIfFound(self):
        t = ("{% tinycontent 'foobar' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("This is a test.",
                         render_template(t))

    def testAlternateTextIfFoundDoubleQuotes(self):
        t = ('{% tinycontent "foobar" %}'
             'I could not find it.'
             '{% endtinycontent %}')

        self.assertEqual("This is a test.",
                         render_template(t))

    def testAlternateTextIfNotFoundSupportsOtherTags(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find {{ meaning }}."
             "{% endtinycontent %}")

        ctx = {'meaning': 42}

        self.assertEqual("I could not find 42.",
                         render_template_with_context(t, ctx))

    def testAllowsContextVariablesAsContentName(self):
        t = ("{% tinycontent_simple content_name %}")

        ctx = {'content_name': 'foobar'}

        self.assertEqual("This is a test.",
                         render_template_with_context(t, ctx))

    def testAllowsContextVariablesAsContentNameFromComplex(self):
        t = ("{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}")

        ctx = {'content_name': 'foobar'}

        self.assertEqual("This is a test.",
                         render_template_with_context(t, ctx))

    def testAllowsUnprovidedContextVariablesAsContentNameFromComplex(self):
        t = ("{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}")

        self.assertEqual("Text if empty.",
                         render_template(t))

    def testAllowsUnprovidedContextVariablesAsContentNameFromSimple(self):
        t = ("{% tinycontent_simple content_name %}")

        self.assertEqual("",
                         render_template(t))

    def testWrongNumberOfArguments(self):
        t = ("{% tinycontent %}{% endtinycontent %}")
        with self.assertRaises(TemplateSyntaxError):
            render_template(t)

    def testBadArguments(self):
        t = ("{% tinycontent 'foo %}{% endtinycontent %}")
        with self.assertRaises(TemplateSyntaxError):
            render_template(t)

        t = ('{% tinycontent "foo %}{% endtinycontent %}')
        with self.assertRaises(TemplateSyntaxError):
            render_template(t)
