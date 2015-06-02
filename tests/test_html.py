import pytest

from .utils import render_template


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
