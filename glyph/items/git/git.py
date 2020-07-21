"""Git Items."""

import os
import typing as T
from dataclasses import dataclass, field

from git import Repo
from git.exc import InvalidGitRepositoryError

from ...item import Item
from ...colors import colorize, Foreground


def find_git():
    try:
        return Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        return None


# TODO: metaclass for automatic dispatch?
@dataclass
class GitItem(Item):
    """Get Git Info."""

    _repo: Repo = field(default_factory=find_git)
    branch: bool = True
    dirty: bool = True
    dirty_symbol: str = "*"

    def get(self) -> T.Dict[str, str]:
        """Get the git information."""
        _repr = {}
        if self._repo is not None:
            if self.branch:
                _repr["branch"] = self._repo.active_branch.name.strip()
            if self.dirty:
                _repr["dirty"] = self.dirty_symbol
        return _repr

    @colorize(foreground_color=Foreground.CYAN)
    def __repr__(self) -> str:
        _repr = self.get()
        return " ".join(
            _repr.get(k, "") for k, v in self.__dict__.items() if not callable(v)
        ).strip()
