import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from tinycontent.models import TinyContent, TinyContentFileUpload
from ..utils import render_template


TEST_FILTER = 'tinycontent.filters.builtin.uploaded_file_filter'


@pytest.mark.django_db
def test_with_uploaded_file_filter(settings, file_upload):
    settings.TINYCONTENT_FILTER = TEST_FILTER

    TinyContent.objects.get_or_create(
        name='fileref',
        content='This is a @file:%s' % file_upload.slug
    )

    result = render_template(
        "{% tinycontent_simple 'fileref' %}"
    )

    prefix = 'This is a <a href="'
    assert result[:len(prefix)] == prefix
    assert file_upload.file.url in result
    assert file_upload.name in result


@pytest.mark.django_db
def test_with_uploaded_file_multiple_files(settings):
    settings.TINYCONTENT_FILTER = TEST_FILTER

    file1 = TinyContentFileUpload.objects.create(
        name='File 1',
        file=SimpleUploadedFile(
            'simple_file.txt', b'Hello, world!'
        )
    )

    file2 = TinyContentFileUpload.objects.create(
        name='File 2',
        file=SimpleUploadedFile(
            'simple_file.txt', b'Hello, world!'
        )
    )

    TinyContent.objects.get_or_create(
        name='multifileref',
        content='This is a @file:file-1\nSo\'s this @file:file-2.'
    )

    result = render_template(
        "{% tinycontent_simple 'multifileref' %}"
    )

    assert 'Download File 1' in result
    assert 'Download File 2' in result
    assert file1.file.url in result
    assert file2.file.url in result


@pytest.mark.django_db
def test_with_uploaded_file_filter_badfile(settings, file_upload):
    settings.TINYCONTENT_FILTER = TEST_FILTER

    TinyContent.objects.get_or_create(
        name='fileref',
        content='This is a @file:hohohoho'
    )

    result = render_template(
        "{% tinycontent_simple 'fileref' %}"
    )

    assert result == 'This is a @file:hohohoho'
