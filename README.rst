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

.. _django-boxes: https://github.com/eldarion/django-boxes
