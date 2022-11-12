#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle automated git actions.
"""

import pathlib

from blib import bcli
from blib import berr

__version__ = "1.0.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Production"


def git_init(repo_path: pathlib.PosixPath) -> None:
    """Initialize a git repo at the filepath if not already created."""
    bcli.create_dir_if_missing(repo_path)
    bcli.run(['git', '-C', repo_path, 'init'])


def git_add(repo_path: pathlib.PosixPath, file: pathlib.PosixPath) -> None:
    """Add filepath to a given git repository."""
    bcli.create_dir_if_missing(repo_path)
    cmd = bcli.run(['git', '-C', repo_path, 'add', str(file)])
    if 'fatal' in cmd.stdout:
        berr.report_error(f'git add failed: {str(file)}')


def git_commit(repo_path: pathlib.PosixPath, message: str = 'backup iA Writer') -> None:
    """Commit to a git repository set by repo_dir."""
    bcli.create_dir_if_missing(repo_path)
    cmd = bcli.run(['git', '-C', repo_path, 'commit', '-m', message])
    if 'nothing to commit' in cmd.stdout:
        berr.report_error('git commit failed')
