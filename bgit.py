#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle automated git actions.

Override repository directory within calling scripts using `bgit.REPO_PATH`.
If one is not given, an error folder will be created on the user's Desktop.
"""

import pathlib

from blib import bcli
from blib import berr
from blib import bfile

__version__ = "1.0.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Testing"

REPO_PATH = pathlib.Path(pathlib.Path().home() / "Desktop" / "errors")


def git_init(repo: pathlib.PosixPath) -> None:
    """Initialize a git repo at the filepath if not already created."""
    global REPO_PATH
    bfile.create_dir_if_missing(REPO_PATH)
    bcli.run(['git', '-C', REPO_PATH, 'init'])


def git_add(file: pathlib.PosixPath) -> None:
    """Add filepath to a given git repository."""
    global REPO_PATH
    bfile.create_dir_if_missing(REPO_PATH)
    cmd = bcli.run(['git', '-C', REPO_PATH, 'add', str(file)])
    if 'fatal' in cmd.stdout:
        berr.report_error(f'git add failed: {str(file)}')


def git_commit(message: str = f"automated commit by {bcli.SCRIPT_NAME}") -> None:
    """Commit to a git repository set by repo_dir."""
    global REPO_PATH
    bfile.create_dir_if_missing(REPO_PATH)
    cmd = bcli.run(['git', '-C', REPO_PATH, 'commit', '-m', message])
    if 'nothing to commit' in cmd.stdout:
        berr.report_error('git commit failed')
