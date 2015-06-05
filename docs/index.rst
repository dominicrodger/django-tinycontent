django-tinycontent
******************

django-tinycontent is a simple Django application for re-usable
content blocks, much like `django-boxes`_.

Blocks are configured via the Django admin, and are available to use
in templates::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'welcome' %}

That template fragment will look for a content block called
``welcome``, and display the content of it.

Optionally, you can post-process the output with :ref:`filters`.


Contents
========

.. toctree::
   :maxdepth: 2

   installation
   templates
   managing_blocks
   filters
   changelog

.. _django-boxes: https://github.com/eldarion/django-boxes
