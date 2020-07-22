"""A CLI prompt."""

import typing as T
from enum import Enum
import os
import pickle

from .item import Item
from .registry import Registry
from . import const
from .items.glyph_error import GlyphErrorItem


class InfoLocation(Enum):
    """Where the information is located relative to the prompt."""

    OFF = 0
    ABOVE = 1
    INLINE = 2


class Prompt:
    """A CLI prompt.

    Args:
        info_location: Where the info items are to be displayed in the prompt
        prompt_str: The final character-sequence before the command

    """

    def __init__(
        self,
        info_location: InfoLocation = InfoLocation.ABOVE,
        prompt_string: str = "%",
        info_separator: str = ":",
        items: T.Optional[T.Dict[str, T.Dict]] = None,
        registry_cache_path: str = const.REGISTRY_CACHE_PATH,
    ):
        self.info_location = InfoLocation(info_location)
        self.info_separator = info_separator
        self.prompt_string = prompt_string
        self.items: T.List[Item] = []

        if os.path.exists(os.path.expanduser(registry_cache_path)):
            with open(os.path.expanduser(registry_cache_path), "rb") as registry_fp:
                try:
                    self.registry = pickle.load(registry_fp)
                except ImportError:
                    # The registry is referring to a plugin that isn't installed
                    self.registry = Registry()
        else:
            self.registry = Registry()

        # Validate
        if items is not None:
            for item, config in items.items():
                try:
                    _item = None
                    try:
                        _item = self.registry.get(item)(**config)
                    except KeyError:
                        self.registry = Registry()
                        _item = self.registry.get(item)(**config)
                    self.items.append(_item)
                except KeyError:
                    self.items.append(GlyphErrorItem(f"Failed to load {item}"))

    def __repr__(self) -> str:
        prompt_str = " "
        if self.info_location is not InfoLocation.OFF:
            # Print Info
            prompt_str += f" {self.info_separator} ".join(
                repr(i) for i in self.items if repr(i).strip()
            )
            if self.info_location is InfoLocation.ABOVE:
                prompt_str += "\n"
        prompt_str += f" {self.prompt_string} "
        return prompt_str
