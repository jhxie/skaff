#!/usr/bin/env python3

"""
A suite of manual pages processing tools.
"""

# ------------------------------- MODULE INFO ---------------------------------
__all__ = [
    "manual_check",
    "manuals_install",
    "manuals_probe",
    "manpath_select"
]
# ------------------------------- MODULE INFO ---------------------------------

# --------------------------------- MODULES -----------------------------------
import gzip
import os
import shutil
import subprocess
import sys

from filecmp import dircmp
from tempfile import TemporaryDirectory
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def manual_check(manual):
    """
    Checks whether 'manual' actually is a valid unix man-page format manual;
    returns boolean value True if so, False otherwise.

    Files that are considered to be unix manual page format must end with file
    extensions that are solely consists of digits 1 to 9 excluding 0.

    NOTE: Man-page section 9 is a non-POSIX standard (convention adopted by
    both Linux and FreeBSD) commonly used for documenting "Kernel Routines".
    """
    if not isinstance(manual, str):
        raise TypeError("'manual' argument must be of 'str' type")

    # The "lazy evaluation" property of the builtin 'all' function ensures that
    # the second lambda would NEVER be evaluated just in case 'x' is a string
    # of zero length
    qualifiers = [
        lambda x: True if 2 == len(x) else False,
        lambda x: True if x[-1] in map(str, range(1, 10)) else False]

    file_extension = os.path.splitext(manual)[-1]

    if all(qualifier(file_extension) for qualifier in qualifiers):
        return True
    else:
        return False


def manuals_install(directory, rebuild=True, *manuals):
    """
    Installs the gzipped manual page(s) in 'manuals' to the subdirectory of
    'directory' that ends with an extra manual section number if it exists;
    for example, if one of the basename of manual in 'manuals' is named 'git.1'
    and a subdirectory '/usr/share/man/man1/' exists, it will be installed to
    that subdirectory instead; otherwise falls back to '/usr/share/man/'.

    If 'rebuild' is set to True, also invokes the 'mandb' program to rebuild
    the manual page index cache.

    If '--record' flag exists in sys.argv, writes the list of installed manual
    pages to the file following the '--record' flag (setuptools compatibility).

    NOTE: It is callers' responsibility to ensure the proper write permission
    is satisfied for the 'directory' (affected by the real UID of the current
    process) and all the subdirectories of it that ends with an extra manual
    section number (see the example above); both 'directory' and all the
    'manuals' must already exist.
    """
    if 0 == len(manuals):
        return

    if not directory.endswith(os.sep):
        directory += os.sep

    if not os.path.isdir(directory):
        raise NotADirectoryError("{0} is not a directory".format(directory))

    if not os.access(directory, os.W_OK):
        raise PermissionError(("The real UID of the current process does not "
                               " permit write operation for "
                               "directory {0}".format(directory)))

    if "--record" in sys.argv:
        with open(sys.argv[sys.argv.index("--record") + 1], "a") as log_output:
            _manuals_copy(directory, log_output, *manuals)
    else:
        _manuals_copy(directory, None, *manuals)

    if rebuild:
        # Finally rebuild the manual page index cache
        with open(os.devnull, "w") as dump:
            return_code = subprocess.call(["mandb"], stdout=dump, stderr=dump)

        if 0 != return_code:
            raise RuntimeError("'mandb' program does not exit properly")


def _manuals_copy(directory, log=None, *manuals):
    """
    Copies the gzipped manual page(s) in 'manuals' to the subdirectory of
    'directory' that ends with an extra manual section number if it exists;
    for example, if one of the basename of manual in 'manuals' is named 'git.1'
    and a subdirectory '/usr/share/man/man1/' exists, it will be installed to
    that subdirectory instead; otherwise falls back to '/usr/share/man/'.

    Also invokes the 'write' method of 'log' to append the file names of
    gzipped manual page(s) copied if 'log' is not None.
    """
    # Based on example from
    # https://docs.python.org/3/library/gzip.html
    for manual in manuals:
        if not manual_check(manual):
            raise TypeError(("The manual page {0} ".format(manual) +
                             "is not in unix 'manpage' format"))
        if not os.path.isfile(manual):
            raise FileNotFoundError(("The manual page {0} ".format(manual) +
                                     "does not exist"))

        # Test whether there exists extra manual subdirectory ends with
        # manual section number; for example,
        # '/usr/share/man/man1/'
        # if so, use this subdirectory instead; otherwise fall back to
        # '/usr/share/man/'
        path_postfix = os.path.splitext(manual)[-1][-1]
        man_subdir = directory + "man" + path_postfix + os.sep

        if os.path.isdir(man_subdir) and os.access(man_subdir, os.W_OK):
            target_manpage = man_subdir + os.path.basename(manual) + ".gz"
        else:
            target_manpage = directory + os.path.basename(manual) + ".gz"

        with open(manual, "rb") as input_manpage:
            with gzip.open(target_manpage, "wb") as output_manpage:
                shutil.copyfileobj(input_manpage, output_manpage)
        if log:
            log.write(target_manpage)


def manuals_probe(*directories):
    """
    Probes all directory specified in 'directories' and returns a sorted list
    containing all the manual page(s) found.
    All the manual page(s) returned are prefixed by absolute path(s).

    NOTE: This function does not recurse more than one level deep into the
    'directories' specified; the order in the result does not necessarily
    correspond to the order the directory appears in 'directories', the results
    are sorted by the builtin 'sorted' function.
    """
    result_manuals = set()

    for directory in directories:
        if not os.path.isdir(directory):
            raise NotADirectoryError("Directory '{0}' does not exist".format(
                directory))
        if not os.path.isabs(directory):
            directory = os.path.abspath(directory)
        if not directory.endswith(os.sep):
            directory += os.sep
        # Here only 'file_list' is used; an alternative would be 'os.listdir';
        # however, that function is not able to distinguish between files and
        # directories, so an extra filter is required, which is less efficient
        for directory_name, subdir_list, file_list in os.walk(directory):
            for candidate in file_list:
                if manual_check(candidate):
                    result_manuals.add(directory + candidate)
            break

    return sorted(result_manuals)


def manpath_select(select=True):
    """
    Parses the output of the 'manpath' program and returns one of its non-empty
    results (non-empty directory) if 'select' is set to True; otherwise returns
    all the results un-altered.

    NOTE: A platform-dependent path separator will be appended to the result.
    """
    paths = None
    result_manpath = None

    with os.popen("manpath") as proc, TemporaryDirectory() as tmpdir:
        paths = proc.read().strip().split(os.pathsep)
        if select:
            for candidate in paths:
                # "Elect" the candidate directory with "rich" non-empty status
                if dircmp(candidate, tmpdir).left_only:
                    result_manpath = candidate
                    break

    if not paths:
        raise RuntimeError("Output of the 'manpath' program cannot be parsed")

    if select and not result_manpath:
        raise RuntimeError("All the directories in 'manpath' is empty")

    if select:
        if result_manpath.endswith(os.sep):
            return result_manpath
        else:
            return result_manpath + os.sep
    else:
        return [path + os.sep for path in paths if not path.endswith(os.sep)]
# -------------------------------- FUNCTIONS ----------------------------------
