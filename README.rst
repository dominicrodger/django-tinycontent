django-tinycontent is a simple Django application for re-usable
content blocks, much like `django-boxes`_.

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
transformed content.

django-tinycontent supports Django 1.4 and Django 1.5. Python 2.6
works with both versions of Django, and Python 3.3 is supported for
Django 1.5.

.. _django-boxes: https://github.com/eldarion/django-boxes
