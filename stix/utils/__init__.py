# Copyright (c) 2015, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

# stdlib
import collections
import contextlib
import keyword

# external
import cybox
import lxml.etree

# internal
import stix


CDATA_START = "<![CDATA["
CDATA_END = "]]>"

_CONFLICTING_NAMES = keyword.kwlist + ['id', 'type','range']


@contextlib.contextmanager
def ignored(*exceptions):
    """Allows you to ignore exceptions cleanly using context managers. This
    exists in Python 3.

    """
    try:
        yield
    except exceptions:
        pass


def strip_cdata(text):
    """Removes all CDATA blocks from `text` if it contains them.

    Note:
        If the function contains escaped XML characters outside of a
        CDATA block, they will be unescaped.

    Args:
        A string containing one or more CDATA blocks.

    Returns:
        An XML unescaped string with CDATA block qualifiers removed.

    """
    xml = "<e>%s</e>" % text
    node = lxml.etree.fromstring(xml)
    return node.text


def cdata(text):
    """Wraps the input `text` in a <![CDATA[]]> block.

    If the text contains CDATA sections already, they are stripped and replaced
    by the application of an outer-most CDATA block.

    Args:
        text: A string to wrap in a CDATA block.

    Returns:
        The `text` value wrapped in <![CDATA[]]>

    """
    if not text:
        return

    if CDATA_START in text:
        text = strip_cdata(text)

    escaped = "{0}{1}{2}".format(CDATA_START, text, CDATA_END)
    return escaped


def is_stix(entity):
    """Returns true if `entity` is an instance of :class:`stix.Entity`."""
    return isinstance(entity, stix.Entity)


def is_cybox(entity):
    """Returns true if `entity` is an instance of :class:`cybox.Entity`."""
    return isinstance(entity, cybox.Entity)


def is_entity(entity):
    """Returns true if `entity` is an instance of :class:`stix.Entity` or
    :class:`cybox.Entity`.

    """
    return isinstance(entity, (cybox.Entity, stix.Entity))


def is_entitylist(entity):
    """Returns true if `entity` is an instance of :class:`stix.EntityList`
    or :class:`cybox.EntityList`.

    """
    return isinstance(entity, (cybox.EntityList, stix.EntityList))


def is_typedlist(entity):
    """Returns true if `entity` is an instance of :class:`stix.TypedList`

    """
    return isinstance(entity, stix.TypedList)


def attr_name(name):
    """Converts `name` into the form expected for python-stix and
    python-cybox properties.

    This is used when attempting to access the property getter/setter via
    the __dict__ instance var entries.

    Example:
        >>> attr_name("id")
        'id_'
        >>> attr_name("Title")
        'title

    """
    name = name.lower()

    if name.startswith("_"):
        name = name[1:]

    if name in _CONFLICTING_NAMES:
        name += "_"

    return name


def key_name(name):
    """Converts the input attribute name `name` into a key to be
    used in `to_dict()` return dictionaries.

    """
    name = attr_name(name)

    if name.endswith("_"):
        return name[:-1]

    return name


def is_sequence(item):
    """Returns ``True`` if `value` is a sequence type (e.g., ``list``, or
    ``tuple``). String types will return ``False``.

    """
    return (
        hasattr(item, "__iter__") and
        not isinstance(item, collections.Mapping)
    )


def check_version(expected, found):
    """Raises ValueError if `found` is not equal to or found within
    `expected`.

    """
    if is_sequence(expected):
        good = found in expected
    else:
        good = (found == expected)

    if good:
        return

    error = "Version '{0}' is invalid. Expected {1}."
    error = error.format(found, expected)
    raise ValueError(error)


def iter_vars(obj):
    return dict(
        (attr_name(x), y) for x, y in obj.__dict__.iteritems() if y
    ).iteritems()


def is_dictable(obj):
    return hasattr(obj, "to_dict") and hasattr(obj, "from_dict")


def is_timestamp(obj):
    return isinstance(obj, datetime.datetime)


def is_etree(obj):
    return isinstance(obj, lxml.etree._Element)


from .nsparser import *
from .dates import *
from .idgen import *
from .nsparser import *
from .walk import *