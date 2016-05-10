import os
import sys

import pytest
from django.core.exceptions import ImproperlyConfigured

from .utils import render_template

# Needed for the custom filter tests
sys.path.append(os.path.dirname(__file__))


@pytest.mark.django_db
def test_with_custom_filter_simple(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'utils.toupper'
    assert "THIS IS A TEST." == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_complex(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'utils.toupper'
    assert "THIS IS A TEST." == render_template(
        "{% tinycontent 'foobar' %}"
        "Not found."
        "{% endtinycontent %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_simple_with_html(html_content, settings):
    settings.TINYCONTENT_FILTER = 'utils.toupper'
    assert "<STRONG>&AMP;</STRONG>" == render_template(
        "{% tinycontent_simple 'html' %}"
    )


@pytest.mark.django_db
def test_with_custom_filter_complex_with_html(html_content, settings):
    settings.TINYCONTENT_FILTER = 'utils.toupper'
    assert "<STRONG>&AMP;</STRONG>" == render_template(
        "{% tinycontent 'html' %}"
        "Not found."
        "{% endtinycontent %}"
    )


@pytest.mark.django_db
def test_with_bad_custom_filter(simple_content, settings):
    settings.TINYCONTENT_FILTER = 'utils.ohnothisisfake'
    with pytest.raises(ImproperlyConfigured):
        render_template("{% tinycontent_simple 'foobar' %}")


@pytest.mark.django_db
def test_with_chained_custom_filters(simple_content, settings):
    settings.TINYCONTENT_FILTER = [
        'utils.toupper',
        'utils.truncate_ten',
        'utils.reverse',
    ]

    assert "A SI SIHT" == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )
