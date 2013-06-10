from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def _imported_symbol(import_path):
    """Resolve a dotted path into a symbol, and return that.

    For example...

    >>> _imported_symbol('django.db.models.Model')
    <class 'django.db.models.base.Model'>

    Raise ImportError if there's no such module, AttributeError if no
    such symbol.

    """
    module_name, symbol_name = import_path.rsplit('.', 1)
    module = import_module(module_name)
    return getattr(module, symbol_name)


def import_from_setting(setting_name):
    """Return the resolution of an import path stored in a Django
    setting. Raises an AttributeError if the setting does not exist.

    :arg setting_name: The name of the setting holding the import path

    Raise ImproperlyConfigured if a path is given that can't be
    resolved.

    """
    path = getattr(settings, setting_name)

    try:
        return _imported_symbol(path)
    except (ImportError, AttributeError):
        raise ImproperlyConfigured('No such module or attribute: %s' % path)
