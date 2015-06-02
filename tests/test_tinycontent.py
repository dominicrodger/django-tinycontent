import pytest

from django.template.base import TemplateSyntaxError

from tinycontent.models import TinyContent
from .utils import render_template


@pytest.mark.django_db
def test_str(simple_content):
    assert "foobar" == str(TinyContent.objects.get(name='foobar'))


@pytest.mark.django_db
def test_non_existent(simple_content):
    assert "" == render_template("{% tinycontent_simple 'foo' %}")


@pytest.mark.django_db
def test_simple_existent(simple_content):
    assert "This is a test." == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )


@pytest.mark.django_db
def test_wrong_number_of_arguments(simple_content):
    t = ("{% tinycontent %}{% endtinycontent %}")

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


@pytest.mark.django_db
def test_with_html_simple(html_content):
    assert "<strong>&amp;</strong>" == render_template(
        "{% tinycontent_simple 'html' %}"
    )


@pytest.mark.django_db
def test_with_html_complex(html_content):
    assert "<strong>&amp;</strong>" == render_template(
        "{% tinycontent 'html' %}"
        "Not found."
        "{% endtinycontent %}"
    )
