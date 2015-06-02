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
