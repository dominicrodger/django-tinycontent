from django.template import Context, Template
from tinycontent.models import TinyContent
import unittest


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context()
    return t.render(c)


class TinyContentTestCase(unittest.TestCase):
    def testNonExistent(self):
        self.assertEqual("",
                         render_template("{% tinycontent 'foobar' %}"))

    def testSimpleExistent(self):
        TinyContent.objects.create(name='foobar',
                                   content='This is a test.')

        self.assertEqual("This is a test.",
                         render_template("{% tinycontent 'foobar' %}"))
