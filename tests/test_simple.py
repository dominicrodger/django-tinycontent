import pytest

from .utils import render_template


@pytest.mark.django_db
def test_non_existent(simple_content):
    assert "" == render_template("{% tinycontent_simple 'foo' %}")


@pytest.mark.django_db
def test_simple_existent(simple_content):
    assert "This is a test." == render_template(
        "{% tinycontent_simple 'foobar' %}"
    )


@pytest.mark.django_db
def test_simple_with_space(simple_content_with_space):
    assert "This is a test with a space." == render_template(
        "{% tinycontent_simple 'foo bar' %}"
    )
