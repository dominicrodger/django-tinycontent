import pytest
from django.contrib.auth.models import User, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from tinycontent.models import TinyContent, TinyContentFileUpload


@pytest.fixture()
def simple_content():
    content, _ = TinyContent.objects.get_or_create(
        name='foobar',
        content='This is a test.'
    )
    return content


@pytest.fixture()
def simple_content_with_space():
    content, _ = TinyContent.objects.get_or_create(
        name='foo bar',
        content='This is a test with a space.'
    )
    return content


@pytest.fixture()
def split_content():
    content, _ = TinyContent.objects.get_or_create(
        name='foo:bar',
        content='This is a second test.'
    )
    return content


@pytest.fixture()
def html_content():
    content, _ = TinyContent.objects.get_or_create(
        name='html',
        content='<strong>&amp;</strong>'
    )
    return content


@pytest.fixture()
def user():
    user, _ = User.objects.get_or_create(username='dom')

    add_perm = Permission.objects.get(
        codename='add_tinycontent'
    )
    change_perm = Permission.objects.get(
        codename='change_tinycontent'
    )

    user.user_permissions.add(add_perm)
    user.user_permissions.add(change_perm)
    user.save()

    return user


@pytest.fixture()
def user_noauth():
    user, _ = User.objects.get_or_create(username='barry')

    return user


@pytest.fixture()
def file_upload():
    upload, _ = TinyContentFileUpload.objects.get_or_create(
        name='Foobar',
        file=SimpleUploadedFile(
            'simple_file.txt', b'Hello, world!'
        )
    )

    return upload
