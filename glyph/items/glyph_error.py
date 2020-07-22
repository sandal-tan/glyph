"""Display an error message as an item."""

from dataclasses import dataclass

from ..item import Item
from ..colors import colorize, Foreground


@dataclass
class GlyphErrorItem(Item):
    """Display a Glyph error as an Item.

    Attributes:
        error: The error as a string

    """

    error: str

    def get(self) -> str:
        """Get the error message."""
        return self.error

    @colorize(foreground_color=Foreground.RED)
    def __repr__(self) -> str:
        return self.get()
