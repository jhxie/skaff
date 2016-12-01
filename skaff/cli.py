#!/usr/bin/env python3

"""
Main command line driver program for skaff.
"""

# --------------------------------- MODULES -----------------------------------
import argparse
import os
import sys

from skaff.clitools import SmartFormatter
from skaff.config import SkaffConfig
from skaff.driver import skaff_drive
from skaff.info import (
    skaff_description_get,
    skaff_info_get
)
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def main() -> None:
    """
    Parses and validates command line option flags, then calls 'skaff_drive'.
    """
    # if "posix" != os.name:
    #     sys.exit("This program is only mean to be used on POSIX systems.")

    skaff_cli_description = skaff_description_get(short=True)
    skaff_cli_dict = dict()

    # Fall back to SmartFormatter to let the string returned
    # by 'skaff_info_get()' function print properly
    parser = argparse.ArgumentParser(description=skaff_cli_description,
                                     formatter_class=SmartFormatter,
                                     prog="skaff")
    parser.add_argument("-a",
                        "--authors",
                        type=str,
                        nargs="+",
                        required=False,
                        help="author(s) of the project")
    parser.add_argument("directories",
                        type=str,
                        nargs="+",
                        help="name(s) for the output project-directory(ies)")
    parser.add_argument("-x",
                        "--language",
                        type=str,
                        required=False,
                        choices=SkaffConfig.languages_fetch(),
                        help="major programming language used")
    parser.add_argument("-l",
                        "--license",
                        type=str,
                        required=False,
                        choices=SkaffConfig.licenses_fetch(),
                        help="type of license")
    parser.add_argument("-q",
                        "--quiet",
                        action="store_true",
                        required=False,
                        help=("no interactive "
                              "CMakeLists.txt and Doxyfile editing"))
    parser.add_argument("-V",
                        "--version",
                        action="version",
                        version=skaff_info_get(),
                        help="print version of skaff and exit")

    args = parser.parse_args()

    # Processing all the "non-private" attributes of args and store them into
    # the 'skaff_cli_dict' dictionary to be passed as arguments
    for attr in filter(lambda attr: not attr.startswith('_'), dir(args)):
        skaff_cli_dict[attr] = getattr(args, attr)

    config = SkaffConfig(**skaff_cli_dict)
    skaff_drive(config)
# -------------------------------- FUNCTIONS ----------------------------------


if __name__ == "__main__":
    main()
