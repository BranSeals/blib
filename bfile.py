#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle file input and output.
"""

import os
import pathlib

__version__ = "0.0.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Dev"


def get_file_list(filepath: pathlib.PosixPath) -> list[str]:
    """Return list of files in a given directory.

    Questions:
        * Q: Do I need to separate by files/directories for this script?
    """
    return os.listdir(filepath)


def create_dir_if_missing(directory: pathlib.PosixPath) -> None:
    """Create a directory if one does not exist."""
    if not pathlib.Path(directory).exists():
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
