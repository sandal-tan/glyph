"""Python virtualenv information."""

from dataclasses import dataclass
import os

from ..item import Item
from ..colors import colorize, Foreground


@dataclass
class VenvItem(Item):

    compact: bool = True

    def get(self) -> str:
        venv_path = os.getenv("VIRTUAL_ENV")
        if venv_path is None:
            venv_path = ""
        return venv_path

    @colorize(foreground_color=Foreground.BLUE)
    def __repr__(self) -> str:
        _repr = self.get()
        if self.compact:
            _repr = os.path.basename(_repr)
        return _repr
