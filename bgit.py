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

__version__ = "1.1.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Testing"

REPO_PATH = pathlib.Path(pathlib.Path().home() / "Desktop" / "errors")


def git_init(repo_path: pathlib.PosixPath = None) -> None:
    """Initialize a git repository if absent.
    """
    global REPO_PATH
    repo = repo_path or REPO_PATH

    bfile.create_dir_if_missing(repo)
    if not pathlib.Path(repo, '.git').exists():
        bcli.run(["git", "-C", repo, "init"])


def git_add(
    file: pathlib.PosixPath = ".",
    repo_path: pathlib.PosixPath = None
) -> None:
    """Stage changes in a git repository.
    """
    global REPO_PATH
    repo = repo_path or REPO_PATH

    bfile.create_dir_if_missing(repo)
    cmd = bcli.run(["git", "-C", repo, "add", str(file)])
    if "fatal" in cmd.stdout:
        berr.report_error(f"git add failed: {str(file)}")


def git_commit(
    message: str = f"auto-commit by {bcli.SCRIPT_NAME}",
    repo_path: pathlib.PosixPath = None,
) -> None:
    """Commit changes to a git repository.
    """
    global REPO_PATH
    repo = repo_path or REPO_PATH

    bfile.create_dir_if_missing(repo)
    cmd = bcli.run(["git", "-C", repo, "commit", "-m", message])
    if "nothing to commit" in cmd.stdout:
        berr.report_error("git commit failed")


def git_add_all_and_commit(
    message: str = f"auto-commit by {bcli.SCRIPT_NAME}",
    repo_path: pathlib.PosixPath = None,
) -> None:
    """Stage and commit all changes to a git repository.
    """
    global REPO_PATH
    repo = repo_path or REPO_PATH

    git_init(repo)
    git_add('.', repo)
    git_commit(f'all changes committed by by {bcli.SCRIPT_NAME}', repo)
