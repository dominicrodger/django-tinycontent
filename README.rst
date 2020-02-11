.. image:: https://travis-ci.org/dominicrodger/django-tinycontent.svg
    :target: https://travis-ci.org/dominicrodger/django-tinycontent

.. image:: https://coveralls.io/repos/dominicrodger/django-tinycontent/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/dominicrodger/django-tinycontent?branch=master

django-tinycontent is a simple Django application for re-usable
content blocks, much like django-boxes.

Installation is simple::

    pip install django-tinycontent

Add ``tinycontent`` to your ``INSTALLED_APPS``.

Usage in templates is simple::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'content_name' %}

Or, to specify a value if a content block by the given name cannot be
found, use::

    {% load tinycontent_tags %}

    {% tinycontent 'content_name' %}
    This will be shown if no matching object is found.
    {% endtinycontent %}

The name of the content block can also be a context variable, using
both the simple and the complex variants.

Content blocks themselves can be added and edited using Django's admin
interface. If a block with the name given in the template tag cannot
be found, either nothing is rendered (if using
``tinycontent_simple``), or the text between ``tinycontent`` and
``endtinycontent`` is rendered (if using the more complex variant).

To apply custom filters to your content, set ``TINYCONTENT_FILTER`` to
a dotted path to a callable that takes the raw content and returns the
transformed content. You can also set ``TINYCONTENT_FILTER`` to be a
list of dotted paths to callables, to chain filters together.

django-tinycontent supports all versions of Django from 2.0 to
3.0. Python 3.6, 3.7 and 3.8 are supported.
