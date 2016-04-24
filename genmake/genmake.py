#!/usr/bin/env python3

# --------------------------------- MODULES -----------------------------------
import os
import pwd
import shutil
import sys

from datetime import datetime
# --------------------------------- MODULES -----------------------------------


def genmake(author, directories, language, license):
    """
    Create all the necessary subdirectories in addition to the project root.
    """
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
        _conf_spawn(language, base_dir)

        for sub_dir in subdirectories:
            os.mkdir(base_dir + sub_dir)

        # Create parent directory if it does not exist
        os.makedirs(base_dir + "include/" + os.path.basename(base_dir[:-1]))


def _license_sign(author, directory, license):
    """
    Copy the license chosen by the 'author' to the 'directory' and sign it with
    'author' with current year prepended if applicable.

    If the license is not specified, default to GPLv3.
    """
    licenses = set(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
    bsd_copyright = "Copyright (c) {0}, {1}\n"

    if 0 == len(directory) or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    # If the license is left as empty, default to GPLv3.
    if 0 == len(license):
        license = "gpl3"
    elif license not in licenses:
        raise ValueError("Invalid license choice")

    # If the author's name is not explicitly stated in the commmand-line
    # argument, default to the GECOS field, which normally stands for the
    # full username of the current user; otherwise fall back to login name.
    pw_record = None
    if not author:
        author = pwd.getpwuid(os.getuid()).pw_gecos
        pw_record = pwd.getpwuid(os.getuid())

        if pw_record.pw_gecos:
            author = pw_record.pw_gecos
        else:
            author = pw_record.pw_name

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


def _conf_spawn(language, directory):
    """
    Spawn configuration files .editorconfig and .gitignore under the project
    root directory.
    """
    languages = set(("c", "cxx"))

    if 0 == len(language):
        language = "c"
    elif language not in languages:
        raise ValueError("Invalid language argument")

    if 0 == len(directory) or not os.path.isdir(directory):
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
