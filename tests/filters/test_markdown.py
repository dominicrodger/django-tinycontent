import pytest

from tinycontent.models import TinyContent
from ..utils import render_template


TEST_FILTER = 'tinycontent.filters.md.markdown_filter'


@pytest.mark.django_db
def test_with_markdown_filter_simple(simple_content, settings):
    settings.TINYCONTENT_FILTER = TEST_FILTER
    assert "<p>This is a test.</p>" == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )


@pytest.mark.django_db
def test_with_markdown_filter_newline(settings):
    settings.TINYCONTENT_FILTER = TEST_FILTER

    TinyContent.objects.get_or_create(
        name='newline',
        content='This is a test.\nHello'
    )

    assert "<p>This is a test.<br />\nHello</p>" == render_template(
        "{% tinycontent_simple 'newline' %}"
    )
