# Standard Library imports

# Core Django imports

# Third-party imports
import bleach

# App imports


def strip_xss(text):
    """ Remove all markup from text. """

    allowed_tags = []
    allowed_attributes = []
    allowed_styles = []

    text = bleach.clean(text, allowed_tags, allowed_attributes, allowed_styles, strip=True, strip_comments=True).strip()

    return text


def string_to_boolean(x):
    """ Return either a boolean or None, based on the user's intent. """

    if isinstance(x, bool):
        return x

    if x is None:
        return None

    if x in [ "null", "Null", "none", "None" ]:
        return None
    if x in [ "true", "True", "1" ]:
        return True
    elif x in [ "false", "False", "0" ]:
        return False
    raise Exception
