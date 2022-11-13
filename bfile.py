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


def get_file_list_str(filepath: pathlib.PosixPath) -> list[str]:
    """Return list of files in a given directory.

    Questions:
        * Q: Do I need to separate by files/directories for this script?
    """
    return os.listdir(filepath)


def listdir(path: str) -> list[pathlib.PosixPath]:
    """List full filepaths from a directory in pathlib format.

    TODO: How is this different from abovein terms of usefulness? Test it.
    """
    filenames = os.listdir(path)
    filepaths = []
    if filenames:
        for f in filenames:
            filepaths.append(pathlib.Path(path, f))
    return filepaths


def create_dir_if_missing(directory: pathlib.PosixPath) -> bool:
    """Create a directory if one does not exist.

    Returns True if directory was created."""
    if not pathlib.Path(directory).exists():
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    else:
        return False


def load_content(filepath: pathlib.PosixPath) -> str:
    with open(filepath, 'r') as f:
        return f.read()
