Release Notes
=============

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
