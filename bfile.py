#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle file input and output.
"""

import pathlib

__version__ = "0.2.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Dev"


def list_dir_filenames(directory: pathlib.Path) -> list[str]:
    """
    Return list of filenames in a given directory.

    Questions:
        * Q: Do I need to separate by files/directories for this script?
    """
    filenames = []
    files = pathlib.Path(directory).iterdir()
    if files:
        for f in files:
            filenames.append(f.name)
    return filenames


def list_dir_filepaths(directory: str) -> list[pathlib.Path]:
    """
    List full filepaths from a directory in pathlib format.
    """
    filepaths = []
    files = pathlib.Path(directory).iterdir()
    if files:
        for f in files:
            filepaths.append(f)
    return filepaths


def create_dirs_if_missing(*directories) -> bool:
    """
    Create a directory if one does not exist.

    Returns True if directory was created.
    """
    for dir in directories:
        if not pathlib.Path(dir).exists():
            pathlib.Path(dir).mkdir(parents=True, exist_ok=True)


def create_file(filepath: pathlib.Path, content: str = None) -> pathlib.Path:
    """
    Create a file with the given content at the target filepath.
    """
    create_dirs_if_missing(filepath)
    if content:
        pathlib.Path(filepath).write_text(content)
    else:
        pathlib.Path(filepath).touch()


def write_text(filepath: pathlib.Path, content: str = None) -> None:
    """
    Open the file in text mode, append to it, and close the file.
    """
    pathlib.Path(filepath).open(mode='w+').write(content)


def append_text(filepath: pathlib.Path, content: str = None) -> None:
    """
    Open the file in text mode, append to it, and close the file.
    """
    pathlib.Path(filepath).open(mode='a+').write(content)
