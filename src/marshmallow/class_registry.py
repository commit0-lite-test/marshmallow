"""A registry of :class:`Schema <marshmallow.Schema>` classes. This allows for string
lookup of schemas, which may be used with
class:`fields.Nested <marshmallow.fields.Nested>`.

.. warning::

    This module is treated as private API.
    Users should not need to use this module directly.
"""

from __future__ import annotations

import typing

from marshmallow.exceptions import RegistryError

if typing.TYPE_CHECKING:
    from marshmallow import Schema

    SchemaType = typing.Type[Schema]
_registry = {}


def register(classname: str, cls: SchemaType) -> None:
    """Add a class to the registry of serializer classes. When a class is
    registered, an entry for both its classname and its full, module-qualified
    path are added to the registry.

    Example: ::

        class MyClass:
            pass


        register("MyClass", MyClass)
        # Registry:
        # {
        #   'MyClass': [path.to.MyClass],
        #   'path.to.MyClass': [path.to.MyClass],
        # }

    """
    global _registry
    if classname in _registry:
        _registry[classname].append(cls)
    else:
        _registry[classname] = [cls]

    full_path = f"{cls.__module__}.{cls.__name__}"
    if full_path in _registry:
        _registry[full_path].append(cls)
    else:
        _registry[full_path] = [cls]


def get_class(classname: str, all: bool = False) -> list[SchemaType] | SchemaType:
    """Retrieve a class from the registry.

    :raises: marshmallow.exceptions.RegistryError if the class cannot be found
        or if there are multiple entries for the given class name.
    """
    try:
        classes = _registry[classname]
    except KeyError as err:
        raise RegistryError(f"Class with name {classname!r} was not found.") from err

    if all:
        return classes

    if len(classes) > 1:
        raise RegistryError(
            f"Multiple classes with name {classname!r} were found. "
            "Please use the full, module-qualified path."
        )

    return classes[0]
