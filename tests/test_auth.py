import pytest

from django.urls import reverse

from .utils import render_for_test_user


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
