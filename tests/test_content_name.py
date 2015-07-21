import pytest

from .utils import (
    render_template,
    render_template_with_context
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
def test_allows_multiple_arguments_and_variables_from_simple(split_content):
    t = ("{% tinycontent_simple 'foo' var %}")

    ctx = {'var': 'bar'}

    assert "This is a second test." == render_template_with_context(t, ctx)


@pytest.mark.django_db
def test_allows_multiple_arguments_and_variables_from_complex(
        split_content
):
    t = ("{% tinycontent 'foo' key %}"
         "Text if empty."
         "{% endtinycontent %}")

    ctx = {'key': 'bar'}

    assert "This is a second test." == render_template_with_context(t, ctx)


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
