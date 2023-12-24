import pytest
from tinycontent.models import TinyContent


@pytest.mark.django_db
def test_with_custom_verbose_name():
    assert TinyContent._meta.app_config.verbose_name == 'Custom Tiny Content'
