"""The previous commands exit code."""

import os
from dataclasses import dataclass

from ..item import Item
from ..colors import colorize, Foreground

class ExitCodeItem(Item):
    """Get and display the exit code of the previous command.

    Notes:
        This requires an environment variable to contain the status code

    Args:
        display_zero: Whether or not to display `0`

    """

    display_zero: bool = False


    def get(self) -> str:
        """Get the current working directory."""
        return os.getenv('STATUS', '0')

    @colorize(Foreground.RED)
    def __repr__(self) -> str:
        _repr = self.get()
        if _repr == '0':
            if self.display_zero:
                return _repr
            return ''
        return _repr
