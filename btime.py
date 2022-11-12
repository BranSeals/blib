#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handle file input and output.
"""

import datetime

__version__ = "0.1.0"
__author__ = "Bran Seals"
__copyright__ = "Copyright 2022"
__email__ = "bran.seals.dev@gmail.com"
__status__ = "Dev"

DT_FILE_FORMAT = '%Y-%m-%d_%H-%M-%S'


def get_dt():
    """Return a simple datetime object.

    Specify format with `DT_FILE_FORMAT`.
    """
    return datetime.datetime.now().strftime(DT_FILE_FORMAT)


def get_dt_str(**transforms) -> str:
    """Return datetime as a string with optional modification.

    Options:
        * prefix - prepend string to datetime
        * postfix - append string to datetime
    """
    dt_str = str(get_dt())
    for mod, value in transforms.items():
        if mod == "prefix":
            dt_str = value + dt_str
        elif mod == "postfix":
            dt_str = dt_str + value
    return dt_str
