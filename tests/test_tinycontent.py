import os
import pytest
import sys

# Needed for the custom filter tests
sys.path.append(os.path.dirname(__file__))

from django.contrib.auth.context_processors import PermWrapper
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.base import TemplateSyntaxError

from tinycontent.models import TinyContent


def render_template(input):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context()
    return t.render(c).strip()


def render_template_with_context(input, context):
    t = Template("{% load tinycontent_tags %}" + input)
    c = Context(context)
    return t.render(c).strip()


def render_for_test_user(t, user):
    ctx = {'user': user, 'perms': PermWrapper(user), }
    return render_template_with_context(t, ctx)


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
def test_with_user(simple_content, user, user_noauth):
    t = ("{% tinycontent 'foobar' %}"
         "Text if empty."
         "{% endtinycontent %}")

    assert "This is a test." == render_for_test_user(t, user_noauth)

    root_edit_url = reverse('admin:tinycontent_tinycontent_change',
                            args=[simple_content.pk, ])

    rendered = render_for_test_user(t, user)
    assert root_edit_url in rendered
    assert 'Edit' in rendered
    assert "This is a test." in rendered

    t = "{% tinycontent_simple 'foobar' %}"
    rendered = render_for_test_user(t, user)
    assert root_edit_url in rendered
    assert 'Edit' in rendered
    assert "This is a test." in rendered


@pytest.mark.django_db
def test_with_user_for_nonexistent_tag(simple_content, user, user_noauth):
    t = ("{% tinycontent 'notthere' %}"
         "Text if empty."
         "{% endtinycontent %}")

    assert "Text if empty." == render_for_test_user(t, user_noauth)

    root_add_url = reverse('admin:tinycontent_tinycontent_add')

    rendered = render_for_test_user(t, user)
    assert '%s?name=notthere' % root_add_url in rendered
    assert 'Add' in rendered
    assert "Text if empty." in rendered

    t = "{% tinycontent_simple 'notthere' %}"
    rendered = render_for_test_user(t, user)
    assert '%s?name=notthere' % root_add_url in rendered
    assert 'Add' in rendered


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


@pytest.mark.django_db
def test_with_custom_filter_simple(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'test_tinycontent.toupper'
    assert "THIS IS A TEST." == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_complex(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'test_tinycontent.toupper'
    assert "THIS IS A TEST." == render_template(
        "{% tinycontent 'foobar' %}"
        "Not found."
        "{% endtinycontent %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_simple_with_html(html_content, settings):
    settings.TINYCONTENT_FILTER = 'test_tinycontent.toupper'
    assert "<STRONG>&AMP;</STRONG>" == render_template(
        "{% tinycontent_simple 'html' %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_complex_with_html(html_content, settings):
    settings.TINYCONTENT_FILTER = 'test_tinycontent.toupper'
    assert "<STRONG>&AMP;</STRONG>" == render_template(
        "{% tinycontent 'html' %}"
        "Not found."
        "{% endtinycontent %}"
    )


@pytest.mark.django_db
def test_with_bad_custom_filter(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'test_tinycontent.ohnothisisfake'
    with pytest.raises(ImproperlyConfigured):
        render_template("{% tinycontent_simple 'foobar' %}")


def toupper(content):
    return content.upper()
