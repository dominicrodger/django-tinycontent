import pytest


@pytest.mark.django_db
def test_tinycontent_str(simple_content):
    assert "foobar" == str(simple_content)


@pytest.mark.django_db
def test_tinycontentfile_str(file_upload):
    assert "Foobar" == str(file_upload)


@pytest.mark.django_db
def test_tinycontentfile_slug(file_upload):
    assert "foobar" == file_upload.slug
