import pytest


@pytest.mark.django_db
def test_tinycontent_str(simple_content):
    assert "foobar" == str(simple_content)
