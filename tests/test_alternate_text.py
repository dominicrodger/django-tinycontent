import pytest

from .utils import (
    render_template,
    render_template_with_context
)


@pytest.mark.django_db
def test_alternate_text_if_not_found(simple_content):
    t = ("{% tinycontent 'neverexists' %}"
         "I could not find it."
         "{% endtinycontent %}")

    assert "I could not find it." == render_template(t)


@pytest.mark.django_db
def test_alternate_text_if_found(simple_content):
    t = ("{% tinycontent 'foobar' %}"
         "I could not find it."
         "{% endtinycontent %}")

    assert "This is a test." == render_template(t)


@pytest.mark.django_db
def test_alternate_text_if_found_double_quotes(simple_content):
    t = ('{% tinycontent "foobar" %}'
         'I could not find it.'
         '{% endtinycontent %}')

    assert "This is a test." == render_template(t)


@pytest.mark.django_db
def test_alternate_text_if_not_found_with_embedded_tags(simple_content):
    t = ("{% tinycontent 'neverexists' %}"
         "I could not find {{ meaning }}."
         "{% endtinycontent %}")

    ctx = {'meaning': 42}

    assert "I could not find 42." == render_template_with_context(
        t, ctx
    )
