Using Blocks in Templates
-------------------------

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
