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
    """
    genmake_cli_description = "Generate a CMake-Based C/C++ Project Structure"
    genmake_cli_dict = {"author": str(),
                        "directories": set(),
                        "language": str(),
                        "license": str()}

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

    args = parser.parse_args()
    arg_attrs = (args.author, args.directories, args.language, args.license)

    for dict_key, arg_attr in zip(sorted(genmake_cli_dict.keys()), arg_attrs):
        if arg_attr:
            genmake_cli_dict[dict_key] = arg_attr

    genmake(**genmake_cli_dict)

main()
