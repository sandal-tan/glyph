"""The previous commands exit code."""

import os
from dataclasses import dataclass
import sys

from ..item import Item
from ..colors import colorize, Foreground

@dataclass
class ExitCodeItem(Item):
    """Get and display the exit code of the previous command.

    Notes:
        This requires an environment variable to contain the status code

    Args:
        display_zero: Whether or not to display `0`
        exit_code_variable: The environment variable containing the status code

    """

    display_zero: bool = False
    exit_code_variable: str = 'exit_code'


    def get(self) -> str:
        """Get the current working directory."""
        return os.getenv(self.exit_code_variable, '0')

    @colorize(Foreground.RED)
    def __repr__(self) -> str:
        _repr = self.get()
        if _repr == '0':
            if self.display_zero:
                return _repr
            return ''
        return _repr
