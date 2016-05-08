#!/usr/bin/env python3

"""
Main command line driver program for genmake.
"""

# --------------------------------- MODULES -----------------------------------
import argparse
import os
import sys

from genmake import genmake, genmake_version_get
# --------------------------------- MODULES -----------------------------------


def main():
    """
    Parse and validate command line option flags, then invoke 'genmake()'.
    """
    genmake_cli_description = "CMake-Based C/C++ Project Structure Generator"
    genmake_cli_dict = dict()

    if "posix" != os.name:
        sys.exit("This script is only mean to be used on POSIX systems.")

    # Fall back to SmartFormatter to let the string returned
    # by 'genmake_version_get()' function print properly
    parser = argparse.ArgumentParser(description=genmake_cli_description,
                                     formatter_class=SmartFormatter,
                                     prog="GenMake")
    parser.add_argument("-a",
                        "--author",
                        type=str,
                        required=False,
                        help="author of the project")
    parser.add_argument("directories",
                        type=str,
                        nargs="+",
                        help="project base output directories")
    parser.add_argument("-x",
                        "--language",
                        type=str,
                        required=False,
                        choices={"c", "cxx"},
                        help="major programming language used")
    parser.add_argument("-l",
                        "--license",
                        type=str,
                        required=False,
                        choices={"bsd2", "bsd3", "gpl2", "gpl3", "mit"},
                        help="type of license")
    parser.add_argument("-q",
                        "--quiet",
                        action="store_true",
                        required=False,
                        help="no interactive Doxyfile editing")
    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=genmake_version_get(),
                        help="print version of GenMake and exit")

    args = parser.parse_args()

    # Processing all the "non-private" attributes of args and store them into
    # the 'genmake_cli_dict' dictionary to be passed as arguments
    for attr in filter(lambda attr: not attr.startswith('_'), dir(args)):
        genmake_cli_dict[attr] = getattr(args, attr)

    genmake(**genmake_cli_dict)


class SmartFormatter(argparse.HelpFormatter):
    """
    You can only specify one formatter in standard argparse, so you cannot
    both have pre-formatted description (RawDescriptionHelpFormatter)
    and ArgumentDefaultsHelpFormatter.
    The SmartFormatter has sensible defaults (RawDescriptionFormatter) and
    the individual help text can be marked ( help="R|" ) for
    variations in formatting.
    Version string is formatted using _split_lines and preserves any
    line breaks in the version string.
    """
    # Use a custom formatter to ensure the custom formatted version string
    # got printed properly while still preserves line-wrapping and other
    # functionality for all the rest of the help text
    # Borrowed from
    # https://bitbucket.org/ruamel/std.argparse/overview
    def __init__(self, *args, **kw):
        self._add_defaults = None
        super(SmartFormatter, self).__init__(*args, **kw)

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        if text.startswith('D|'):
            self._add_defaults = True
            text = text[2:]
        elif text.startswith('*|'):
            text = text[2:]
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)

    def _get_help_string(self, action):
        if self._add_defaults is None:
            return argparse.HelpFormatter._get_help_string(self, action)
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: %(default)s)'
        return help

    def _expand_help(self, action):
        """
        Mark a password help with '*|' at the start, so that
        when global default adding is activated (e.g. through a helpstring
        starting with 'D|') no password is show by default.
        Orginal marking used in repo cannot be used because of decorators.
        """
        hs = self._get_help_string(action)
        if hs.startswith('*|'):
            params = dict(vars(action), prog=self._prog)
            if params.get('default') is not None:
                # you can update params, this will change the default, but we
                # are printing help only
                params['default'] = '*' * len(params['default'])
            return self._get_help_string(action) % params
        return super(SmartFormatter, self)._expand_help(action)

if __name__ == "__main__":
    main()
