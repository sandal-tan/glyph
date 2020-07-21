"""Discovery of Items."""

from abc import abstractmethod, ABC


class Item(ABC):
    """Abstract base class for all info `Item`s."""

    @abstractmethod
    def get(self) -> str:
        """Get the info for an `Item`."""

    @abstractmethod
    def __repr__(self) -> str:
        """Printable representation of `Item`."""

