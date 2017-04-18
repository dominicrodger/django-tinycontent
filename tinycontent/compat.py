import base64
import django
from django.utils import six


if django.VERSION > (1, 8,):
    # Taken from django-allauth
    # The MIT License (MIT)

    # Copyright (c) 2010-2016 Raymond Penners and contributors

    # Permission is hereby granted, free of charge, to any person
    # obtaining a copy of this software and associated documentation
    # files (the "Software"), to deal in the Software without
    # restriction, including without limitation the rights to use,
    # copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the
    # Software is furnished to do so, subject to the following
    # conditions:

    # The above copyright notice and this permission notice shall be
    # included in all copies or substantial portions of the Software.

    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    # EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    # OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    # HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    # WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    # OTHER DEALINGS IN THE SOFTWARE.
    from django.template.loader import render_to_string
else:
    from django.template.loader import render_to_string as _render_to_string

    # Wire the Django >= 1.8 API to the Django < 1.7 implementation.
    def render_to_string(
            template_name, context=None, request=None, using=None):
        assert (
            using is None,
            "Multiple template engines requires Django >= 1.8"
        )  # flake8: noqa
        assert (
            request is None,
            "Using the request keyword argument requires Django >= 1.8"
        )  # flake8: noqa
        return _render_to_string(template_name, context)


def cache_safe_key(key):
    if six.PY2:
        return base64.b64encode(
            key
        )

    return base64.b64encode(bytes(key, 'utf-8'))
