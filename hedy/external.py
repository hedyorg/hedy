# Manages external dependencies and state for Hedy we might want to inject from
# elsewhere.


def configure_gettext(new_gettext_fn):
    """Sets the gettext function used for translations in Hedy."""
    global gettext
    gettext = new_gettext_fn


# pylint: disable=function-redefined
def gettext(x):
    """Translate the given input.

    Can be configure from outside using 'configure_gettext'."""
    return x  # Default: no translation
