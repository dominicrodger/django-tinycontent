import pytest

from django.template.base import TemplateSyntaxError

from tinycontent.models import TinyContent
from .utils import (
    render_template,
    render_template_with_context
)


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


@pytest.mark.django_db
def test_allows_context_variables_as_content_names_from_simple(simple_content):
    t = ("{% tinycontent_simple content_name %}")

    ctx = {'content_name': 'foobar'}

    assert "This is a test." == render_template_with_context(t, ctx)


@pytest.mark.django_db
def test_allows_context_variables_as_content_names_from_complex(
        simple_content
):
    t = ("{% tinycontent content_name %}"
         "Text if empty."
         "{% endtinycontent %}")

    ctx = {'content_name': 'foobar'}

    assert "This is a test." == render_template_with_context(t, ctx)


@pytest.mark.django_db
def test_allows_with_tag_as_content_names_from_simple(simple_content):
    t = ("{% with content_name='foobar' %}"
         "{% tinycontent_simple content_name %}"
         "{% endwith %}")

    assert "This is a test." == render_template(t)


@pytest.mark.django_db
def test_allows_with_tag_as_content_names_from_complex(simple_content):
    t = ("{% with content_name='foobar' %}"
         "{% tinycontent content_name %}"
         "Text if empty."
         "{% endtinycontent %}"
         "{% endwith %}")

    assert "This is a test." == render_template(t)


@pytest.mark.django_db
def test_allows_unprovided_ctx_variables_as_content_name_complex(
        simple_content
):
    t = ("{% tinycontent content_name %}"
         "Text if empty."
         "{% endtinycontent %}")

    assert "Text if empty." == render_template(t)


@pytest.mark.django_db
def test_allows_unprovided_ctx_variables_as_content_name_simple(
        simple_content
):
    t = ("{% tinycontent_simple content_name %}")

    assert "" == render_template(t)


@pytest.mark.django_db
def test_ctx_variables_with_name_of_content_complex(simple_content):
    t = ("{% tinycontent foobar %}"
         "Text if empty."
         "{% endtinycontent %}")

    assert "Text if empty." == render_template(t)


@pytest.mark.django_db
def test_ctx_variables_with_name_of_content_simple(simple_content):
    t = ("{% tinycontent_simple foobar %}")

    assert "" == render_template(t)


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
