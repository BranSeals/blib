#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Report errors via `mail` utility.

Errors can be collected using `report_error()` and are automatically
mailed to the executing user when this module unloads.

If you have issues with particular files causing false errors (e.g.
while iterating through a file directory) add them to the `ignored`
list to omit any line that contains them.
"""

import atexit

from blib import bcli

print(bcli.SCRIPT_NAME)

__version__ = "1.0.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Production"

errors = []
ignored = [
    '.git',
    '.DS_Store',
]


def report_error(error: str) -> None:
    """Add an entry to the error report."""
    errors.append(error)


def __format_report() -> str:
    """Apply formatting to the emailed error report.

    Using markdown format so [] appears as checkbox if text is copied.
    """
    report = 'Errors:'
    if errors:
        for e in errors:
            report = report + '\n[] ' + e
    return report


@atexit.register
def __send_report() -> None:
    """Send a formatted error report to a system user.

    Removes lines containing elements from `ignored`. Be careful if you
    use generic substrings that appear in error messages, such as "error".

    Future:
        Is there a better way than O(n^2)?
    """
    if errors:
        # Collect indices to remove
        remove_n = []
        for n, line in enumerate(errors):
            for file in ignored:
                if file in line:
                    remove_n.append(n)

        # Remove indices backwards to avoid re-indexing issues
        for i in sorted(remove_n, reverse=True):
            del errors[i]

    # Check again because list could now be empty
    if errors:
        bcli.mail(__format_report(), f'{bcli.SCRIPT_NAME} errors')
