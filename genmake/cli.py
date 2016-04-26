#!/usr/bin/env python3

"""
Main command line driver program for genmake.
"""

# --------------------------------- MODULES -----------------------------------
import argparse
import os
import sys

from genmake import genmake
# --------------------------------- MODULES -----------------------------------


def main():
    """
    Parse and validate command line option flags, then invoke 'genmake()'.
    """
    genmake_cli_description = "CMake-Based C/C++ Project Structure Generator"
    genmake_cli_dict = dict()

    if "posix" != os.name:
        sys.exit("This script is only mean to be used on POSIX systems.")

    parser = argparse.ArgumentParser(description=genmake_cli_description)
    parser.add_argument("-a",
                        "--author",
                        type=str,
                        required=False,
                        help="Author of the Project")
    parser.add_argument("directories",
                        type=str,
                        nargs="+",
                        help="Project Base Output Directories")
    parser.add_argument("-x",
                        "--language",
                        type=str,
                        required=False,
                        choices=set(("c", "cxx")),
                        help="Major Programming Language Used")
    parser.add_argument("-l",
                        "--license",
                        type=str,
                        required=False,
                        choices=set(("bsd2", "bsd3", "gpl2", "gpl3", "mit")),
                        help="Type of License")
    parser.add_argument("-q",
                        "--quiet",
                        action="store_true",
                        required=False,
                        help="Type of License")

    args = parser.parse_args()

    # Processing all the "non-private" attributes of args and store them into
    # the 'genmake_cli_dict' dictionary to be passed as arguments
    for attr in filter(lambda attr: not attr.startswith('_'), dir(args)):
        genmake_cli_dict[attr] = getattr(args, attr)

    genmake(**genmake_cli_dict)


if __name__ == "__main__":
    main()
