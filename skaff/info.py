#!/usr/bin/env python3

"""
A collections of subroutines used for returning information strings of the
skaff package.
"""

# ------------------------------- MODULE INFO ---------------------------------
__all__ = ["skaff_description_get", "skaff_info_get"]
# ------------------------------- MODULE INFO ---------------------------------

# --------------------------------- MODULES -----------------------------------
from datetime import datetime
from skaff import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __version__
)
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def skaff_description_get(short: bool=True) -> str:
    """
    Returns the description string of the skaff program.
    A concise description will be returned if 'short' is set to True; otherwise
    the full version is returned instead.
    """
    short_description = "An Extensible Project Scaffolding Tool"
    long_description = ("Skaff is a Python library for building programming "
                        "language dependent scaffolding of software projects, "
                        "and a command-line tool that uses this library with "
                        "built-in (CMake-based) C/C++ support.")
    if short:
        return short_description
    else:
        return long_description


def skaff_info_get() -> str:
    """
    Returns the copyright information string of the skaff program.
    """
    module_info_dict = {"author": __author__,
                        "email": __email__,
                        "info": skaff_description_get(short=True),
                        "license": __license__,
                        "maintainer": __maintainer__,
                        "version": __version__,
                        "year": datetime.now().year}
    skaff_info = (
        "skaff "
        "({info}) {version}\n"
        "Copyright (C) {year} {author}.\n"
        "Licensed and distributed under the BSD 2-Clause License.\n"
        "This is free software: you are free to change and redistribute it.\n"
        "There is NO WARRANTY, to the extent permitted by law.\n\n"
        "Written by {author}.".format(**module_info_dict))
    return skaff_info
# -------------------------------- FUNCTIONS ----------------------------------
