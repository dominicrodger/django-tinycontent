from django.template import Context, Template
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
    def testNonExistent(self):
        self.assertEqual("",
                         render_template("{% tinycontent_simple 'foobar' %}"))

    def testSimpleExistent(self):
        TinyContent.objects.create(name='foobar',
                                   content='This is a test.')

        self.assertEqual("This is a test.",
                         render_template("{% tinycontent_simple 'foobar' %}"))

    def testAlternateTextIfNotFound(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("I could not find it.",
                         render_template(t))

    def testAlternateTextIfFound(self):
        TinyContent.objects.create(name='test_name',
                                   content='This should be found.')

        t = ("{% tinycontent 'test_name' %}"
             "I could not find it."
             "{% endtinycontent %}")

        self.assertEqual("This should be found.",
                         render_template(t))

    def testAlternateTextIfFoundDoubleQuotes(self):
        TinyContent.objects.create(name='test_name_double',
                                   content='This should be found.')

        t = ('{% tinycontent "test_name_double" %}'
             'I could not find it.'
             '{% endtinycontent %}')

        self.assertEqual("This should be found.",
                         render_template(t))

    def testAlternateTextIfNotFoundSupportsOtherTags(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find {{ meaning }}."
             "{% endtinycontent %}")

        ctx = {'meaning': 42}

        self.assertEqual("I could not find 42.",
                         render_template_with_context(t, ctx))

    def testAllowsContextVariablesAsContentName(self):
        TinyContent.objects.create(name='variable_name',
                                   content='This is a variable test.')
        t = ("{% tinycontent_simple content_name %}")

        ctx = {'content_name': 'variable_name'}

        self.assertEqual("This is a variable test.",
                         render_template_with_context(t, ctx))

    def testAllowsContextVariablesAsContentNameFromComplex(self):
        TinyContent.objects.create(name='another_variable',
                                   content='This is another variable test.')
        t = ("{% tinycontent content_name %}"
             "Text if empty."
             "{% endtinycontent %}")

        ctx = {'content_name': 'another_variable'}

        self.assertEqual("This is another variable test.",
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
