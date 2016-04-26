#!/usr/bin/env python3

"""
Main module of genmake.
"""
# --------------------------------- MODULES -----------------------------------
import os
import pwd
import shutil
import subprocess
import sys

from datetime import datetime
from distuils import spawn
# --------------------------------- MODULES -----------------------------------


def genmake(author, directories, language, license, quiet):
    """
    Create all the necessary subdirectories in addition to the project root.

    All arguments can be 'None' except 'directories', which must be a list of
    strings of length >= 1.

    If the above is the case, 'author' will be guessed by GECOS field and login
    name of the current user; 'language' will default to 'c', 'license' will be
    set to 'bsd2', 'quiet' will be unchanged (equivalent to False).
    """
    if not isinstance(directories, list):
        raise ValueError("'directories' argument must be of list type")
    elif 0 == len(directories):
        raise ValueError("'directories' argument must not be empty")

    subdirectories = (
        "build",
        "coccinelle",
        "doc",
        "img",
        "src",
        "tests"
    )

    for base_dir in directories:
        if "/" != base_dir[-1]:
            base_dir += "/"
        os.mkdir(base_dir)
        _license_sign(author, base_dir, license)
        _conf_spawn(base_dir, language)
        _doc_create(author, base_dir, license, quiet)

        for sub_dir in subdirectories:
            os.mkdir(base_dir + sub_dir)

        # Create parent directory if it does not exist
        os.makedirs(base_dir + "include/" + os.path.basename(base_dir[:-1]))


def _license_sign(author, directory, license):
    """
    Copy the license chosen by the 'author' to the 'directory' and sign it with
    'author' with current year prepended if applicable.

    If the license is not specified, default to BSD 2-clause license.
    """
    licenses = set(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
    bsd_copyright = "Copyright (c) {0}, {1}\n"

    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    # If the license is left as empty, default to BSD 2-clause license.
    if not license:
        license = "bsd2"
    elif license not in licenses:
        raise ValueError("Invalid license choice")

    if not author:
        author = _author_get()

    if not sys.path[0]:
        raise RuntimeError("Current sys.path[0] is empty")

    license_text = sys.path[0] + "/license/" + license + ".txt"
    license_target = directory + "LICENSE.txt"
    if license in set(("bsd2", "bsd3", "mit")):
        with open(license_text, "r") as from_file:
            vanilla_license_text = from_file.read()
            with open(license_target, "w") as to_file:
                date_record = datetime.now()
                to_file.write(bsd_copyright.format(date_record.year, author))
                to_file.write(vanilla_license_text)
    else:
        shutil.copy(license_text, license_target)


def _conf_spawn(directory, language):
    """
    Spawn configuration files under the project root directory.
    """
    languages = set(("c", "cxx"))

    if not language:
        language = "c"
    elif language not in languages:
        raise ValueError("Invalid language argument")

    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    cmake_file = "CMakeLists.txt"
    cmake_source_prefix = sys.path[0] + "/config/" + language + "/"

    shutil.copy(cmake_source_prefix + cmake_file, directory)

    conf_files = ("gitattributes", "gitignore", "editorconfig")
    conf_source_prefix = sys.path[0] + "/config/"
    conf_target_prefix = directory + "."

    for configuration in conf_files:
        shutil.copy(conf_source_prefix + configuration + ".txt",
                    conf_target_prefix + configuration)


def _doc_create(author, directory, license, quiet=False):
    """
    Create 'Doxyfile' and 'README.md' template.

    Launch $EDITOR or vim on the 'Doxyfile' upon completion, can be turned off
    by setting quiet to True.
    """
    licenses = set(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
    # If the license is left as empty, default to BSD 2-clause license.
    if not license:
        license = "bsd2"
    elif license not in licenses:
        raise ValueError("Invalid license choice")

    if not author:
        author = _author_get()

    readme_header = "## Overview\n\n## License\n"
    copyright_line = "Copyright &copy; {0} {1}\n"
    readme_text = directory + "README.md"
    license_text = sys.path[0] + "/license/" + license + ".md"

    with open(license_text, "r") as license_file:
        license_markdown = license_file.read()
        with open(readme_text, "w") as readme_file:
            date_record = datetime.now()
            readme_file.write(readme_header)
            readme_file.write(copyright_line.format(date_record.year, author))
            readme_file.write(license_markdown)

    doxyfile = "Doxyfile"
    doxyfile_source_prefix = sys.path[0] + "/config/"
    doxyfile_target_prefix = directory
    shutil.copy(doxyfile_source_prefix + doxyfile,
                doxyfile_target_prefix + doxyfile)

    if not quiet:
        # Default to 'vi' or 'vim' if the environment variable is not set.
        default_editor = None
        editor_candidates = ("vim", "vi")

        for candidate in editor_candidates:
            if spawn.find_executable(candidate):
                default_editor = candidate
                break

        editor = os.environ.get("EDITOR", default_editor)
        subprocess.call([editor, doxyfile_target_prefix + doxyfile])


def _author_get():
    """
    Get the current logged-in username from GECOS or name field.

    Raise RuntimeError if both attempt fail.
    """
    # If the author's name is not explicitly stated in the commmand-line
    # argument, default to the GECOS field, which normally stands for the
    # full username of the current user; otherwise fall back to login name.
    author = None
    pw_record = None
    pw_record = pwd.getpwuid(os.getuid())

    if pw_record.pw_gecos:
        author = pw_record.pw_gecos
    elif pw_record.pw_name:
        author = pw_record.pw_name

    if author:
        return author
    else:
        raise RuntimeError("Failed attempt to get default username")
