"""CLI entrypoint."""

import os
import sys
from logging import ERROR

import logzero
import yaml

from .prompt import Prompt
from . import const


def cli():
    """CLI Entrypoint."""

    logzero.loglevel(ERROR)

    for loc in const.CONFIG_FILE_LOCATIONS:
        if os.path.exists(loc):
            break
    else:
        raise RuntimeError("Could not find a file.")

    with open(loc) as config_fp:
        obj = yaml.load(config_fp, Loader=yaml.SafeLoader)

    prompt = Prompt(**obj)
    sys.stdout.write(repr(prompt))
