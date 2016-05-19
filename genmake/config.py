#!/usr/bin/env python3

"""
Custom configuration type for the 'core' genmake module.
"""

# --------------------------------- MODULES -----------------------------------
import collections
import os
import pwd
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class GenMakeConfig:
    """
    Configuration type used for the argument of 'genmake' function.
    """

    def __init__(self, **kwargs):
        """
        Constructs a new 'GenMakeConfig' class instance.

        Supported keyword arguments:

        'authors': author(s) of the project(s)

        'directories': name of the output project-directory(ies)

        'language': major programming language used; one of
                    {"c", "cpp"}

        'license': type of license; one of
                    {"bsd2", "bsd3", "gpl2", "gpl3", "mit"}

        'quiet': no interactive CMakeLists.txt and Doxyfile editing
        """
        __ARGUMENTS = {"authors": self.authors_set,
                       "directories": self.directories_set,
                       "language": self.language_set,
                       "license": self.license_set,
                       "quiet": self.quiet_set}
        self.__config = dict()
        for key in __ARGUMENTS:
            # Call corresponding mutator function with value specified in the
            # 'kwargs' dictionary if key is present
            if key in kwargs:
                __ARGUMENTS[key](kwargs[key])
            # Otherwise let the mutator function use default value
            # NOTE: 'directories_set' would raise exception with default
            # 'None' actual parameter
            else:
                __ARGUMENTS[key]()

    def authors_set(self, authors=None):
        """
        Sets the author(s) of the project(s).

        Sets the single author to be the GECOS or name field of current
        logged-in user if 'authors' is left as default or 'None'.
        """
        if None == authors:
            self.__config["authors"] = GenMakeConfig.author_fetch()
            return

        if isinstance(authors, str) and authors and authors.isidentifier():
            self.__config["authors"] = authors
        else:
            raise ValueError("'authors' argument must be non-empty 'str' type")

    def author_get(self):
        """
        Gets the author(s) of the project(s).
        """
        return self.__config["authors"]

    @classmethod
    def author_fetch():
        """
        Gets the current logged-in username from GECOS or name field.

        Raises RuntimeError if both attempts fail.

        Note this 'classmethod' may be automatically called from 'author_get'
        member function under certain scenarios.
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

    def directories_set(self, directories=None):
        """
        Sets the name of the outputting project-directory(ies).

        'directories' argument must be of 'collections.Iterable' type.
        """
        if not isinstance(directories, collections.Iterable):
            raise ValueError("'directories' argument must be iterable")

        if 0 == len(directories):
            raise ValueError("'directories' argument must not be empty")

        if not all(isinstance(directory, str) for directory in directories):
            raise ValueError("'directories' argument must contain 'str' type")

        self.__config["directories"] = directories

    def directories_get(self):
        """
        Gets the name of the outputting project-directory(ies).
        """
        return self.__config["directories"]

    def language_set(self, language=None):
        """
        Sets the major programming language used.
        Defaults to 'c' language if left as empty or 'None'.

        'language' argument must be one of
        {"c", "cpp"}.
        """
        languages = frozenset(("c", "cpp"))

        if None == language:
            self.__config["language"] = "c"
            return

        if language not in languages:
            raise ValueError("'language' argument must be one of 'c' or 'cpp'")

        self.__config["language"] = language

    def language_get(self):
        """
        Gets the major programming language used.
        """
        return self.__config["language"]

    def license_set(self, license=None):
        """
        Sets the type of license.
        Defaults to 'bsd2' license if left as empty or 'None'.

        'license' argument must be one of
        {"bsd2", "bsd3", "gpl2", "gpl3", "mit"}.
        """
        licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))

        if None == license:
            self.__config["license"] = "bsd2"
            return

        if license not in licenses:
            raise ValueError(("'license' choice must be one of the following: "
                              ", ".join(licenses)))

        self.__config["license"] = license

    def license_get(self):
        """
        Gets the type of license.
        """
        return self.__config["license"]

    def quiet_set(self, quiet=None):
        """
        Sets whether there is interactive CMakeLists.txt and Doxyfile editing.
        'True' to turn off the interactive editing.
        Defaults to 'True' if left as empty or 'None'.

        'quiet' argument must be of 'bool' type.
        """
        if None == quiet:
            self.__config["quiet"] = False
            return

        if not isinstance(quiet, bool):
            raise ValueError("'quiet' must be of 'bool' type")

        self.__config["quiet"] = quiet

    def quiet_get(self):
        """
        Gets whether there is interactive CMakeLists.txt and Doxyfile editing.
        """
        return self.__config["quiet"]

    def _load(self, **kwargs):
        """
        """
        pass

    def _save(self, **kwargs):
        """
        """
        pass

# --------------------------------- CLASSES -----------------------------------
