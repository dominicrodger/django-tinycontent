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
transformed content. You can also set ``TINYCONTENT_FILTER`` to be a
list of dotted paths to callables, to chain filters together.

django-tinycontent supports all versions of Django from 1.5 to
1.8. Python 2.7, 3.3 and 3.4 are supported.

Changelog
=========

v0.4.0
------

* Require at least django-autoslug 1.8.0, to fix a warning about
  unapplied migrations.

v0.3.0
------

* Drop support for Django 1.4 (it's quite hard to support Django 1.4
  and 1.9 in a single release - since Django 1.4 requires ``{% load
  url from future %}``, and Django 1.9 doesn't support it).
* Ensure the wheel we upload to PyPI is universal.
* Forward compatibility for Django 1.9 - remove the ``{% load url
  from future %}`` from tinycontent templates.

v0.2.1
------

* Forwards compatibility change for Django 1.9 - which will remove
  the version of ``importlib`` bundled with Django. All supported
  versions of Python (2.7, 3.3 and 3.4) have ``importlib``.

v0.2.0
------

* Dropped support for Python 2.6.
* Added a built-in markdown filter - you can use it by setting
  ``TINYCONTENT_FILTER`` to
  ``'tinycontent.filters.md.markdown_filter'``.
* Added the ability to include links to files which you can upload
  via the admin.
* Added support for setting ``TINYCONTENT_FILTER`` to a list of
  dotted paths, to allow chaining filters.

v0.1.8
------

* Added the ``TINYCONTENT_FILTER`` setting for controlling the way
  content is output.
* Improved testing with Travis (we now test all supported Python
  versions and Django versions).

.. _django-boxes: https://github.com/eldarion/django-boxes
