"""Utilities for printing colored strings."""

from enum import Enum, auto
import typing as T

from . import utils


class Color(Enum):
    """The classic 8 colors."""

    BLACK = 0
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()


@utils.singleton
class Foreground:
    """Apply foreground colors.
    This dynamically generates functions to apply foregrounds colors defined in the `Color` enum to a string
    via calling that color.
    Example:
        >>> from ist.color import Foreground
        >>> Foreground.RED('Hello, World')
        '\x1b[31mHello, world\x1b[0m'
        >>> Foreground.GREEN('Hello, World')
        '\x1b[32mHello, world\x1b[0m'
    """

    def __init__(self):
        self._values = {}
        for color in Color:
            self._values[color.name] = color.value

    def __getattr__(self, name: str) -> T.Callable[[str], str]:
        if name in self._values:
            _apply_color = lambda text: f"\u001b[3{self._values[name]}m{text}\u001b[0m"
            _apply_color.__name__ = name
            return _apply_color
        raise AttributeError(f"Foreground has no such attribute: {name}")


def colorize(foreground_color: Foreground) -> T.Callable:
    """Color the returned string.

    Args:
        foreground_color: The color to use for the foreground

    Returns:
        The decorator for applying ``foreground_color`` to a function

    """

    def _decorate(func: T.Callable):
        def _call(*args, **kwargs):
            return foreground_color(func(*args, **kwargs))

        return _call

    return _decorate
