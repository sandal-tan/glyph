"""An Item for the current working directory."""

import os
from pathlib import Path
from dataclasses import dataclass

from ..item import Item
from ..colors import colorize, Foreground


@dataclass
class DirItem(Item):
    """Get and display the current working directory.

    Args:
        expand_user: Whether or not to expand `~` to `$HOME`
        compact: Whether or not to truncate parent directory names

    """

    expand_user: bool = False
    compact: bool = True

    def get(self) -> str:
        """Get the current working directory."""
        return os.getcwd()

    @colorize(Foreground.GREEN)
    def __repr__(self) -> str:
        _repr = self.get()
        if not self.expand_user:
            _repr = _repr.replace(str(Path.home()), "~")
        return _repr
