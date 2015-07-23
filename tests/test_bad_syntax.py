import pytest

from django.template.base import TemplateSyntaxError

from .utils import render_template


@pytest.mark.django_db
def test_wrong_number_of_arguments(simple_content):
    t = ("{% tinycontent %}{% endtinycontent %}")

    with pytest.raises(TemplateSyntaxError):
        render_template(t)


@pytest.mark.django_db
def test_wrong_number_of_arguments_simple(simple_content):
    t = ("{% tinycontent_simple %}")

    with pytest.raises(TemplateSyntaxError):
        render_template(t)


@pytest.mark.django_db
def test_bad_arguments(simple_content):
    t = ("{% tinycontent 'foo %}{% endtinycontent %}")
    with pytest.raises(TemplateSyntaxError):
        render_template(t)

    t = ('{% tinycontent "foo %}{% endtinycontent %}')
    with pytest.raises(TemplateSyntaxError):
        render_template(t)
