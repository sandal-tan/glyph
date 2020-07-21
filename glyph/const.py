"""Glyph Constants."""

import typing as T
import os
import pkg_resources

REGISTRY_CACHE_PATH: str = "~/.cache/glyph/registry.pckl"

CONFIG_FILE_LOCATIONS: T.List[str] = [
    os.path.expanduser("~/.glyph.yaml"),
    os.path.expanduser("~/.glyph.yml"),
    pkg_resources.resource_filename(__name__, "glyph.yaml"),
]
