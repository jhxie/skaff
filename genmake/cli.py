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
    genmake_cli_dict = {"author": str(),
                        "directories": set(),
                        "language": str(),
                        "license": str(),
                        "quiet": False}

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
    arg_attrs = (args.author,
                 args.directories,
                 args.language,
                 args.license,
                 args.quiet)

    for dict_key, arg_attr in zip(sorted(genmake_cli_dict.keys()), arg_attrs):
        if arg_attr:
            genmake_cli_dict[dict_key] = arg_attr

    genmake(**genmake_cli_dict)


if __name__ == "__main__":
    main()
