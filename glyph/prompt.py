"""A CLI prompt."""

from dataclasses import dataclass
import typing as T
from enum import Enum

from .item import Item
from .registry import Registry


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
    ):
        self.info_location = InfoLocation(info_location)
        self.info_separator = info_separator
        self.prompt_string = prompt_string
        self.items: T.List[Item] = []
        self.registry = Registry()

        # Validate
        if items is not None:
            for item, config in items.items():
                self.items.append(self.registry.get(item)(**config))

    def __repr__(self) -> str:
        prompt_str = " "
        if self.info_location is not InfoLocation.OFF:
            # Print Info
            prompt_str += f" {self.info_separator} ".join(
                repr(i) for i in self.items if repr(i)
            )
            if self.info_location is InfoLocation.ABOVE:
                prompt_str += "\n "
        prompt_str += self.prompt_string + " "
        return prompt_str
