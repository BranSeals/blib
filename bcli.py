#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle console commands.
"""

import __main__
import os
import pathlib
import pwd
import subprocess

__version__ = "0.1.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Dev"

SCRIPT_NAME = pathlib.Path(__main__.__file__).stem
USER = pwd.getpwuid(os.getuid()).pw_name


def run(list_: list[str], str_: str = None):
    """Run console command using a list of components.

    Assign this function to a value for stdout and stderr.

    Future:
        Accept a string with a normal command format, then break it up
        into a list within this function. It would have to be safe to
        use with spaces intact where required (i.e. ignored in quotes).

    Note:
        I saw a quiz question once that used a stack for tracking open
        and closed parentheses. Maybe use a stack for any character
        that requires closing? Something like: "if item on stack,
        don't split this space"? Would need a lot of testing with
        commands that have a lot of nested statements, like a
        database command.
    """
    return subprocess.run(
        list_,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        input=str_
    )


def mail(body: str, subject: str = SCRIPT_NAME, user: str = USER) -> None:
    """Send system mail to the user."""
    run(['mail', '-s', subject, user], body)
