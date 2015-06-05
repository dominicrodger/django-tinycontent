Adding and Editing Blocks
-------------------------

Content blocks themselves can be added and edited using Django's
admin interface. If a block with the name given in the template tag
cannot be found, either nothing is rendered (if using
``tinycontent_simple``), or the text between ``tinycontent`` and
``endtinycontent`` is rendered (if using the more complex variant).

If you're logged in as a user with permission to add or edit content
blocks (which you can set via permissions in the Django admin),
you'll see links to the admin page for adding blocks (if there's no
block set up yet) or editing (if the content block already exists).
