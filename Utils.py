"""
Holds various common functions and variables which will be useful in general
by the other classes.
"""

import sys
from io import StringIO
from contextlib import contextmanager, closing


COALA_KEY = "coala-sublime"


def log(*args, **kwargs):
    print(" COALA -", *args, **kwargs)


@contextmanager
def replace_stdout(replacement):
    """
    Replaces stdout with the replacement, yields back to the caller
    and then reverts everything back.
    """
    _stdout = sys.stdout
    sys.stdout = replacement
    try:
        yield
    finally:
        sys.stdout = _stdout


@contextmanager
def retrieve_stdout():
    """
    Yields a StringIO object that stdout has been redirected to.
    """
    with closing(StringIO()) as sio, replace_stdout(sio):
        yield sio
