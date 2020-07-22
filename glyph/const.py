"""Glyph Constants."""

import typing as T
import os
from importlib import resources

REGISTRY_CACHE_PATH: str = "~/.cache/glyph/registry.pckl"

with resources.path("glyph", "glyph.yaml") as resource_path:
    CONFIG_FILE_LOCATIONS: T.List[str] = [
        os.path.expanduser("~/.glyph.yaml"),
        os.path.expanduser("~/.glyph.yml"),
        str(resource_path),
    ]
