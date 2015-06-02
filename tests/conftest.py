# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest
from tinycontent.models import TinyContent


@pytest.fixture()
def simple_content():
    return TinyContent.objects.get_or_create(
        name='foobar',
        content='This is a test.'
    )


@pytest.fixture()
def html_content():
    return TinyContent.objects.get_or_create(
        name='html',
        content='<strong>&amp;</strong>'
    )
