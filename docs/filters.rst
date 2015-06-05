.. _filters:

Filters
=======

By default, no transformations are applied to the content blocks -
they're just displayed as they were entered in the admin. Since you
probably want to display HTML, you'll probably want to set up a
filter to apply before displaying content blocks, such as Markdown.

.. contents::
   :local:

Specifying Filters
------------------

You can configure what filter is applied using the setting
``TINYCONTENT_FILTER``, which should be set to a dotted path to a
function to call to filter the content (for example, to convert
Markdown to HTML).

.. warning::

   If the given path is invalid, any use of tinycontent tags will
   raise ``ImproperlyConfigured``. If this setting is not provided,
   the content will be returned exactly as stored.

For example, if your project has a file called ``utils.py``, you might
have a function in it called ``tinycontent_transform`` that would look
something like this::

    def tinycontent_transform(content):
        return do_something_to(content)

To get the tinycontent templates to use that function, in your
``settings.py`` file, you'd write something like::

    TINYCONTENT_FILTER = 'myproj.utils.tinycontent_transform'

Chaining Filters
----------------

You can optionally set ``TINYCONTENT_FILTER`` to a list of dotted
paths - filters will be applied in the order in which you provide
them.

For example, to use :ref:`markdown-filter` with tinycontent's
:ref:`built-in file support <file-filter>`, you could set
``TINYCONTENT_FILTER`` like this::

    TINYCONTENT_FILTER = [
        'tinycontent.filters.md.markdown_filter',
        'tinycontent.filters.builtin.uploaded_file_filter',
    ]

Built-in Filters
----------------

.. _markdown-filter:

Markdown
^^^^^^^^

django-tinycontent ships with a filter for Markdown. You can enable
this by setting ``TINYCONTENT_FILTER`` like this::

    TINYCONTENT_FILTER = 'tinycontent.filters.md.markdown_filter'

.. _file-filter:

File-upload Handler
^^^^^^^^^^^^^^^^^^^

The file-upload filter replaces instances of ``@file:slug`` (where
``slug`` is the slug of a TinyContentFileUpload) with the URL to the
file.

You can enable this filter by setting ``TINYCONTENT_FILTER`` like
this::

    TINYCONTENT_FILTER = 'tinycontent.filters.builtin.uploaded_file_filter'
