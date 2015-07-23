Using Blocks in Templates
=========================

Usage in templates is simple - to show the content of a block called
``content_name`` you can just use the template tag
``tinycontent_simple``::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'content_name' %}

Or, to specify a value if a content block by the given name cannot be
found, use the ``tinycontent`` tag::

    {% load tinycontent_tags %}

    {% tinycontent 'content_name' %}
    This will be shown if no matching object is found.
    {% endtinycontent %}

The name of the content block can also be a context variable, using
both the simple and the complex variants.

Optionally, you can post-process the output with :ref:`filters`.

.. _multiple-arguments:

Passing Multiple Arguments
--------------------------

.. versionadded:: 0.5

You can pass multiple arguments to the django-tinycontent template
tags, like this::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'content_name' 'extra' %}

Extra arguments are concatenated together before looking up the
content block - the above example will look for a content block
called ``content_name:extra``.

The main use case for this is internationalisation - each argument
can either be a string literal (as in our example above), or a
context variable. For example - to include the language code as part
of your block name, you could use::

    {% load tinycontent_tags %}

    {% tinycontent_simple 'content_name' request.LANGUAGE_CODE %}

For those of us running websites in Great Britain, that would result
in fetching the content block ``content_name:en-gb``.

This feature is available both for ``tinycontent_simple``, and
``tinycontent``.
