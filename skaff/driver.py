#!/usr/bin/env python3

"""
Main driver module of the skaff program.
"""

# ------------------------------- MODULE INFO ---------------------------------
__all__ = ["skaff_drive", "skaff_version_get"]
# ------------------------------- MODULE INFO ---------------------------------

# --------------------------------- MODULES -----------------------------------
import collections
import os
import re
import shutil
import subprocess
import tempfile

from datetime import datetime
from distutils import spawn
from skaff.clitools import (
    getkey,
    timeout,
    ANSIColor,
    TimeOutError
)
from skaff.config import SkaffConfig
from skaff import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __version__
)
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def skaff_drive(config):
    """
    Creates all the necessary subdirectories in addition to the project root.
    """
    if not isinstance(config, SkaffConfig):
        raise ValueError("'config' argument must be of 'SkaffConfig' type")

    for base_dir in config.directories_get():
        os.makedirs(base_dir)
        for sub_dir in config.subdirectories_get():
            os.makedirs(base_dir + sub_dir)
        # Create parent directory if it does not exist
        os.makedirs("{0}include{1}{2}".format(base_dir,
                                              os.sep,
                                              os.path.basename(base_dir[:-1])))
        _license_sign(base_dir, config)
        _conf_doc_prompt(base_dir, config)


def skaff_version_get():
    """
    Returns the version information string of the skaff program.
    """
    module_info_dict = {"author": __author__,
                        "email": __email__,
                        "license": __license__,
                        "maintainer": __maintainer__,
                        "version": __version__,
                        "year": datetime.now().year}
    skaff_version_info = (
        "skaff "
        "(A CMake-based project scaffolding tool) {version}\n"
        "Copyright (C) {year} {author}.\n"
        "Licensed and distributed under the BSD 2-Clause License.\n"
        "This is free software: you are free to change and redistribute it.\n"
        "There is NO WARRANTY, to the extent permitted by law.\n\n"
        "Written by {author}.".format(**module_info_dict))
    return skaff_version_info


def _arguments_check(directory, config):
    """
    Performs 3 separate checks for the input 'directory' and 'config':
    1. Whether 'directory' actually exist in the physical file system.
    2. Whether 'config' is a (sub)class instance of 'SkaffConfig'.
    3. Whether 'directory' can be obtained by 'directories_get' member function
    call.
    """
    if not os.path.isdir(directory):
        raise ValueError("'directory' must already exist")

    if not isinstance(config, SkaffConfig):
        raise ValueError("'config' argument must be of 'SkaffConfig' type")

    if directory not in config.directories_get():
        raise ValueError(("'directory' argument must appear in the result of "
                          "'directories_get()' member function invocation"))


def _conf_doc_prompt(directory, config):
    """
    Prints interactive prompt related to the current 'directory' if 'quiet' is
    False.

    Calls '_conf_spawn' and '_doc_create()' with the arguments given
    afterwards.
    """
    _arguments_check(directory, config)

    terminal_info = shutil.get_terminal_size()
    hints = list()
    hints.append("Upcoming Configuration Editing for {0}{1}{2}".format(
        ANSIColor.KHAKI, directory, ANSIColor.RESET))
    hints.append("The editing will start after [{0}{1}{2}].".format(
        ANSIColor.BLUE, "5 seconds", ANSIColor.RESET))
    hints.append("Press [{0}c{1}] to continue the editing.".format(
        ANSIColor.PURPLE, ANSIColor.RESET))
    hints.append("Press [{0}k{1}] to skip the upcoming directory.".format(
        ANSIColor.PURPLE, ANSIColor.RESET))
    hints.append("Press [{0}a{1}] to skip all the rest.".format(
        ANSIColor.PURPLE, ANSIColor.RESET))
    key = str()
    quiet = config.quiet_get()

    if not quiet:
        os.system("clear")
        print("-" * terminal_info.columns + "\n")
        for line in hints:
            print(line.center(terminal_info.columns))
        print("\n" + "-" * terminal_info.columns)
        try:
            while "c" != key.lower():
                key = timeout(5)(getkey)()
                if "a" == key.lower() or "k" == key.lower():
                    config.quiet_set(True)
                    break
        except TimeOutError:
            pass
        os.system("clear")

    _conf_spawn(directory, config)
    _doc_create(directory, config)

    # Revert the changes if only the current 'directory' is affected
    # by the 'quiet' setting
    if "k" == key.lower():
        config.quiet_set(False)


def _conf_edit(directory, conf_files):
    """
    Edits all the 'conf_files' under 'directory' interactively.

    By default the environment variable 'EDITOR' is used; if it is empty,
    fall back to either 'vim' or 'vi'.
    """
    if not directory or not os.path.isdir(directory):
        raise ValueError("'directory' must already exist")

    if not directory.endswith(os.sep):
        directory += os.sep

    if not isinstance(conf_files, collections.Iterable):
        raise ValueError("'conf_files' argument must be of iterable type")
    elif 0 == len(conf_files):
        raise ValueError("'conf_files' argument must not be empty")

    # Default to 'vi' or 'vim' if the environment variable is not set.
    default_editor = None
    editor_candidates = ("vim", "vi")

    for candidate in editor_candidates:
        if spawn.find_executable(candidate):
            default_editor = candidate
            break

    editor = os.environ.get("EDITOR", default_editor)

    for conf_file in conf_files:
        subprocess.call([editor, directory + conf_file])


def _conf_spawn(directory, config):
    """
    Spawns configuration files under the project root directory.

    The spawned configuration files in the project root include:
    {
    ".editorconfig", ".gdbinit", ".gitattributes",
    ".gitignore", ".travis.yml", "CMakeLists.txt"
    }

    An additional "CMakeLists.txt" will also be spawned in 'src' subdirectory
    if it exists.
    """
    _arguments_check(directory, config)

    language = config.language_get()
    quiet = config.quiet_get()
    cmake_file = "CMakeLists.txt"
    cmake_source_prefix = SkaffConfig.basepath_fetch() +\
        "config" + os.sep +\
        "template" + os.sep +\
        language + os.sep
    sample_source_file = "main." + language

    shutil.copy(cmake_source_prefix + cmake_file, directory)

    if os.path.isdir(directory + "src"):
        shutil.copy(cmake_source_prefix + "src" + os.sep + cmake_file,
                    directory + "src" + os.sep)
        shutil.copy(cmake_source_prefix + "src" + os.sep + sample_source_file,
                    directory + "src" + os.sep)

    # Again, "figuring out where the configuration resides" may belong to the
    # responsibility of 'SkaffConfig' class; this responsibiltiy will be
    # moved to 'SkaffConfig' after "ini-parsing" functionality is implemented.
    conf_files = ("editorconfig", "gdbinit", "gitattributes", "gitignore")
    conf_source_prefix = SkaffConfig.basepath_fetch() +\
        "config" + os.sep +\
        "template" + os.sep
    conf_target_prefix = directory + "."
    travis_file = "travis.yml"
    language_header = "language: {0}\n".format(language)

    for configuration in conf_files:
        shutil.copy(conf_source_prefix + configuration + ".txt",
                    conf_target_prefix + configuration)

    with open(conf_source_prefix + travis_file, "r") as travis_source:
        travis_text = travis_source.read()
        with open(conf_target_prefix + travis_file, "w") as travis_target:
            travis_target.write(language_header)
            travis_target.write(travis_text)
    if not quiet:
        _conf_edit(directory, [cmake_file])


def _doc_create(directory, config):
    """
    Creates 'CHANGELOG.md', 'Doxyfile', and 'README.md' template.

    Launches $EDITOR or vim on the 'Doxyfile' upon completion, can be turned
    off by setting quiet to True.
    """
    _arguments_check(directory, config)

    changelog_header = (
        "# Change Log\n"
        "This document records all notable changes to {0}.  \n"
        "This project adheres to [Semantic Versioning](http://semver.org/).\n"
        "\n## 0.1 (Upcoming)\n"
        "* New feature here\n"
    ).format(directory[:-1].title())
    readme_header = (
        "![{0}](misc{1}img{1}banner.png)\n"
        "\n## Overview\n"
        "\n## License\n"
    ).format(directory[:-1], os.sep)
    changelog_text = directory + "CHANGELOG.md"
    copyright_line = "Copyright &copy; {year} {authors}\n".format(
        year=datetime.now().year,
        authors=", ".join(config.authors_get())
    )
    license_text = SkaffConfig.basepath_fetch() +\
        "config" + os.sep +\
        "license" + os.sep +\
        config.license_get() + ".md"
    readme_text = directory + "README.md"

    with open(license_text, "r") as license_file:
        license_markdown = license_file.read()
        with open(readme_text, "w") as readme_file:
            readme_file.write(readme_header)
            readme_file.write(copyright_line)
            readme_file.write(license_markdown)

    with open(changelog_text, "w") as changelog_file:
        changelog_file.write(changelog_header)

    _doxyfile_generate(directory, config)


def _doxyfile_attr_match(project_name, line):
    """
    Determines whether there is any 'Doxyfile' options available in 'line'.

    Return the updated version if 'line' contains options that need to be
    changed; otherwise return None.
    """
    arguments = (project_name, line)

    if not all(argument for argument in arguments):
        raise ValueError(("Both 'project_name' and 'line' "
                         "have to be non-empty 'str' type"))

    if not all(isinstance(argument, str) for argument in arguments):
        raise ValueError(("Both 'project_name' and 'line' "
                         "have to be of 'str' type"))

    # Gets rid of the trailing separator character
    if project_name.endswith(os.sep):
        project_name = project_name[:-1]

    # Tests whether the length of 'project_name' become 0 after truncation
    if not project_name:
        raise ValueError("'project_name' cannot be a single slash character")

    attr_dict = {"PROJECT_NAME": "\"" + project_name.title() + "\"",
                 "OUTPUT_DIRECTORY": "." + os.sep + "doc",
                 "TAB_SIZE": 8,
                 "EXTRACT_ALL": "YES",
                 "EXTRACT_STATIC": "YES",
                 "RECURSIVE": "YES",
                 "EXCLUDE": "build",
                 "HAVE_DOT": "YES",
                 "UML_LOOK": "YES",
                 "TEMPLATE_RELATIONS": "YES",
                 "CALL_GRAPH": "YES",
                 "DOT_IMAGE_FORMAT": "svg",
                 "INTERACTIVE_SVG": "YES"}
    line = line.lstrip()

    # If the line is solely composed of whitespace or is a comment
    if not line or line.startswith("#"):
        return None

    for attr in attr_dict:
        # '\s' stands for whitespace characters
        match = re.match(R"\s*" + attr + R"\s*=", line)
        if match:
            split_index = match.string.find("=") + 1
            return match.string[:split_index] + " " +\
                str(attr_dict[attr]) + "\n"

    return None


def _doxyfile_generate(directory, config):
    """
    Generates or uses existing template 'Doxyfile' within 'directory'.

    Launches $EDITOR or vim afterwards if 'quiet' is set to False.
    """
    _arguments_check(directory, config)

    doxyfile = "Doxyfile"
    doxyfile_source_prefix = SkaffConfig.basepath_fetch() +\
        "config" + os.sep +\
        "template" + os.sep
    doxyfile_target_prefix = directory
    doxygen_cmd = ["doxygen", "-g", doxyfile_target_prefix + doxyfile]
    quiet = config.quiet_get()

    if spawn.find_executable("doxygen"):
        # Redirects the terminal output of 'doxygen' to null device
        with open(os.devnull, "w") as null_device:
            subprocess.call(doxygen_cmd, stdout=null_device)
        with tempfile.TemporaryFile("w+") as tmp_file:
            with open(doxyfile_target_prefix + doxyfile, "r+") as output_file:
                for line in output_file:
                    match = _doxyfile_attr_match(directory, line)
                    tmp_file.write(line if not match else match)
                tmp_file.seek(0)
                output_file.seek(0)
                output_file.truncate()
                shutil.copyfileobj(tmp_file, output_file)
    else:
        shutil.copy(doxyfile_source_prefix + doxyfile,
                    doxyfile_target_prefix + doxyfile)

    if not quiet:
        _conf_edit(directory, [doxyfile])


def _license_sign(directory, config):
    """
    Copies the license chosen by authors to the 'directory', signs it
    with authors and current year prepended if applicable; 'directory' must
    already exist.

    Note only licenses in {"bsd2", "bsd3", "mit"} will be signed by names in
    authors.
    """
    _arguments_check(directory, config)

    copyright_line = "Copyright (c) {year}, {authors}\n".format(
        year=datetime.now().year,
        authors=", ".join(config.authors_get())
    )
    # Note "figuring out where the source license resides" may belong to the
    # responsibility of 'SkaffConfig' class; this responsibiltiy will be
    # moved to 'SkaffConfig' after "ini-parsing" functionality is implemented.
    license_source = SkaffConfig.basepath_fetch() +\
        "config" + os.sep +\
        "license" + os.sep +\
        config.license_get() + ".txt"
    license_target = directory + "LICENSE.txt"

    if config.license_get() in frozenset(("bsd2", "bsd3", "mit")):
        with open(license_source, "r") as from_file:
            vanilla_license_text = from_file.read()
            with open(license_target, "w") as to_file:
                to_file.write(copyright_line)
                to_file.write(vanilla_license_text)
    else:
        shutil.copy(license_source, license_target)
# -------------------------------- FUNCTIONS ----------------------------------
