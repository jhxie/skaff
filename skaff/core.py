#!/usr/bin/env python3

"""
Main module of skaff.
"""

# ------------------------------- MODULE INFO ---------------------------------
# Note the naming convention shown here coming from the 'ranger' program from
# http://ranger.nongnu.org/
__author__ = "Jiahui Xie"
__email__ = "jiahui.xie@outlook.com"
__license__ = "BSD"
__maintainer__ = __author__
__version__ = "1.0"
# ------------------------------- MODULE INFO ---------------------------------

# --------------------------------- MODULES -----------------------------------
import os
import pwd
import re
import shutil
import subprocess
import tempfile

from datetime import datetime
from distutils import spawn
from skaff import single_keypress_read
from skaff import timeout
from skaff import ANSIColor
from skaff import SkaffConfig
from skaff import TimeOutError
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def skaff(config):
    """
    Creates all the necessary subdirectories in addition to the project root.
    """
    if not isinstance(config, SkaffConfig):
        raise ValueError("'config' argument must be of 'SkaffConfig' type")

    author = list(config.authors_get())[0]
    language = config.language_get()
    license = config.license_get()
    quiet = config.quiet_get()

    for base_dir in config.directories_get():
        os.mkdir(base_dir)
        for sub_dir in config.subdirectories_get():
            os.mkdir(base_dir + sub_dir)
        # Create parent directory if it does not exist
        os.makedirs("{0}include{1}{2}".format(base_dir,
                                              os.sep,
                                              os.path.basename(base_dir[:-1])))
        _license_sign(author, base_dir, license)
        _conf_doc_prompt(author, base_dir, language, license, quiet)


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
        "Licensed and distributed under BSD 2-Clause License.\n"
        "This is free software: you are free to change and redistribute it.\n"
        "There is NO WARRANTY, to the extent permitted by law.\n\n"
        "Written by {author}.".format(**module_info_dict))
    return skaff_version_info


def _license_sign(author, directory, license):
    """
    Copies the license chosen by the 'author' to the 'directory', signs it
    with 'author' and current year prepended if applicable.

    If the license is not specified, default to BSD 2-clause license.
    """
    licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
    bsd_copyright = "Copyright (c) {0}, {1}\n"

    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    if not directory.endswith(os.sep):
        directory += os.sep

    # If the license is left as empty, default to BSD 2-clause license.
    if not license:
        license = "bsd2"
    elif license not in licenses:
        raise ValueError("Invalid license choice")

    if not author:
        author = _author_get()

    license_text = _basepath_find() + os.sep + "license" + os.sep +\
        license + ".txt"
    license_target = directory + "LICENSE.txt"
    if license in frozenset(("bsd2", "bsd3", "mit")):
        with open(license_text, "r") as from_file:
            vanilla_license_text = from_file.read()
            with open(license_target, "w") as to_file:
                date_record = datetime.now()
                to_file.write(bsd_copyright.format(date_record.year, author))
                to_file.write(vanilla_license_text)
    else:
        shutil.copy(license_text, license_target)


def _conf_spawn(directory, language, quiet):
    """
    Spawns configuration files under the project root directory.
    """
    languages = frozenset(("c", "cpp"))

    if not language:
        language = "c"
    elif language not in languages:
        raise ValueError("Invalid language argument")

    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    if not directory.endswith(os.sep):
        directory += os.sep

    cmake_file = "CMakeLists.txt"
    cmake_source_prefix = _basepath_find() + os.sep +\
        "config" + os.sep +\
        language + os.sep
    sample_source_file = "main." + language

    shutil.copy(cmake_source_prefix + cmake_file, directory)

    if os.path.isdir(directory + "src"):
        shutil.copy(cmake_source_prefix + "src" + os.sep + cmake_file,
                    directory + "src" + os.sep)
        shutil.copy(cmake_source_prefix + "src" + os.sep + sample_source_file,
                    directory + "src" + os.sep)

    conf_files = ("editorconfig", "gdbinit", "gitattributes", "gitignore")
    conf_source_prefix = _basepath_find() + os.sep + "config" + os.sep
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


def _conf_edit(directory, conf_files):
    """
    Edits all the 'conf_files' under 'directory' interactively.

    By default the environment variable 'EDITOR' is used; if it is empty,
    fall back to either 'vim' or 'vi'.
    """
    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    if not directory.endswith(os.sep):
        directory += os.sep

    if not isinstance(conf_files, list):
        raise ValueError("'conf_files' argument must be of list type")
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


def _doc_create(author, directory, license, quiet):
    """
    Creates 'CHANGELOG.md', 'Doxyfile', and 'README.md' template.

    Launches $EDITOR or vim on the 'Doxyfile' upon completion, can be turned
    off by setting quiet to True.
    """
    licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
    # If the license is left as empty, default to BSD 2-clause license.
    if not license:
        license = "bsd2"
    elif license not in licenses:
        raise ValueError("Invalid license choice")

    if not author:
        author = _author_get()

    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    if not directory.endswith(os.sep):
        directory += os.sep

    changelog_header = (
        "# Change Log\n"
        "This document records all notable changes to {0}.  \n"
        "This project adheres to [Semantic Versioning](http://semver.org/).\n"
        "\n## 0.1 (Upcoming)\n"
        "* New feature here\n"
    ).format(directory[:-1].title())
    readme_header = (
        "![{0}](img{1}banner.png)\n"
        "\n## Overview\n"
        "\n## License\n"
    ).format(directory[:-1], os.sep)
    changelog_text = directory + "CHANGELOG.md"
    copyright_line = "Copyright &copy; {0} {1}\n"
    license_text = _basepath_find() + os.sep +\
        "license" + os.sep +\
        license + ".md"
    readme_text = directory + "README.md"

    with open(license_text, "r") as license_file:
        license_markdown = license_file.read()
        with open(readme_text, "w") as readme_file:
            date_record = datetime.now()
            readme_file.write(readme_header)
            readme_file.write(copyright_line.format(date_record.year, author))
            readme_file.write(license_markdown)

    with open(changelog_text, "w") as changelog_file:
        changelog_file.write(changelog_header)

    _doxyfile_generate(directory, quiet)


def _doxyfile_generate(directory, quiet):
    """
    Generates or uses existing template 'Doxyfile' within 'directory'.

    Launches $EDITOR or vim afterwards if 'quiet' is set to False.
    """
    if not directory or not os.path.isdir(directory):
        raise ValueError("Invalid directory argument")

    if not directory.endswith(os.sep):
        directory += os.sep

    doxyfile = "Doxyfile"
    doxyfile_source_prefix = _basepath_find() + os.sep + "config" + os.sep
    doxyfile_target_prefix = directory
    doxygen_cmd = ["doxygen", "-g", doxyfile_target_prefix + doxyfile]

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


def _author_get():
    """
    Gets the current logged-in username from GECOS or name field.

    Raises RuntimeError if both attempts fail.
    """
    # If the author's name is not explicitly stated in the commmand-line
    # argument, default to the GECOS field, which normally stands for the
    # full username of the current user; otherwise fall back to login name.
    author = None
    pw_record = pwd.getpwuid(os.getuid())

    if pw_record.pw_gecos:
        author = pw_record.pw_gecos
    elif pw_record.pw_name:
        author = pw_record.pw_name

    if author:
        return author
    else:
        raise RuntimeError("Failed attempt to get default username")


def _basepath_find():
    """
    Returns the base directory name of the skaff module.

    The extra 'os.path.abspath' invocation is to suppress relative path output.
    """
    return os.path.dirname(os.path.abspath(__file__))


def _conf_doc_prompt(author, directory, language, license, quiet):
    """
    Prints interactive prompt related to the current 'directory' if 'quiet' is
    False.

    Calls '_conf_spawn' and '_doc_create()' with the arguments given
    afterwards.
    """
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

    if not hasattr(_conf_doc_prompt, "skip_rest"):
        _conf_doc_prompt.skip_rest = False

    if _conf_doc_prompt.skip_rest:
        quiet = True

    if not quiet:
        os.system("clear")
        print("-" * terminal_info.columns + "\n")
        for line in hints:
            print(line.center(terminal_info.columns))
        print("\n" + "-" * terminal_info.columns)
        try:
            while "c" != key.lower():
                key = timeout(5)(single_keypress_read)()
                if "a" == key.lower():
                    _conf_doc_prompt.skip_rest = True
                    quiet = True
                    break
                elif "k" == key.lower():
                    quiet = True
                    break
        except TimeOutError:
            pass
        os.system("clear")

    _conf_spawn(directory, language, quiet)
    _doc_create(author, directory, license, quiet)
# -------------------------------- FUNCTIONS ----------------------------------
