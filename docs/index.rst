Welcome to django-tinycontent's documentation!
==============================================

.. toctree::
   :maxdepth: 2

django-tinycontent is a simple Django application for re-usable
content blocks, much like `django-boxes`_.

Installation is simple::

    pip install django-tinycontent

Add ``tinycontent`` to your ``INSTALLED_APPS``.

Usage is simple::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'content_name' %}

Or, to specify a value if a content block by the given name cannot be
found, use::

    {% load tinycontent_tags %}

    {% tinycontent 'content_name' %}
    This will be shown if no matching object is found.
    {% endtinycontent %}

.. _django-boxes: https://github.com/eldarion/django-boxes
