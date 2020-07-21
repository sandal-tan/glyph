"""Discovery of Items."""

import importlib
import pkgutil
import pprint
import pyclbr

from logzero import logger

from . import items
from .item import Item


def discover_namespace_plugins(namespace_package):
    """Get the contents of a namespace package.

    Args:
        Get the `Item` defined in a namespace package

    """
    packages = {}
    logger.debug("Looking for Item in: %s", namespace_package.__name__)

    for _, name, ispkg in pkgutil.iter_modules(
        namespace_package.__path__, f"{namespace_package.__name__}."
    ):
        if ispkg:
            packages = {
                **packages,
                **discover_namespace_plugins(importlib.import_module(name)),
            }

        else:
            _classes = pyclbr.readmodule(name)

            for _class in _classes.values():
                logger.debug("Found class: %s", _class.name)
                for super_class in _class.super:
                    if super_class == "Item":
                        _class_name = f"{name}.{_class.name}"
                        logger.debug("Adding Item: %s", _class_name)
                        packages[_class.name] = getattr(
                            importlib.import_module(name), _class.name
                        )
                        break
    return packages


class Registry:
    """A registry of items."""

    def __init__(self):
        self.items = discover_namespace_plugins(items)

    def __repr__(self):
        return pprint.pformat(self.items)

    def get(self, name: str) -> Item:
        """Get an `Item` from the registry.

        Args:
            name: The name of the item

        Returns:
            The item if it exists

        """
        return self.items[name]
