from django.template import Context, Template
from tinycontent.models import TinyContent
import unittest


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context({'meaning': 42})
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

    def testAlternateTextIfNotFoundSupportsOtherTags(self):
        t = ("{% tinycontent 'neverexists' %}"
             "I could not find {{ meaning }}."
             "{% endtinycontent %}")

        self.assertEqual("I could not find 42.",
                         render_template(t))
