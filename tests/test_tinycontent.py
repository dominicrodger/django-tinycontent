import pytest

from tinycontent.models import TinyContent


@pytest.mark.django_db
def test_str(simple_content):
    assert "foobar" == str(TinyContent.objects.get(name='foobar'))
