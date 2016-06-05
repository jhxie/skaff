#!/usr/bin/env python3

"""
Custom configuration type for the 'core' skaff module.
"""

# --------------------------------- MODULES -----------------------------------
import collections
import os
import pwd
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class SkaffConfig:
    """
    Configuration type used for the argument of 'skaff' function.
    """

    def __init__(self, directories, **kwargs):
        """
        Constructs a new 'SkaffConfig' class instance.

        Note you can also specify 'directories' in keyword arguments;
        the value in keyword arguments will be used instead.

        Required arguments:

        'directories': set of name(s) for the output project-directory(ies)

        Supported keyword arguments:

        'authors': set of author(s) for the project(s)

        'directories': set of name(s) for the output project-directory(ies)

        'language': major programming language used;
                    must be chosen from the 'languages_list' listing.

        'license': type of license;
                    must be chosen from the 'licenses_list' listing.

        'quiet': no interactive CMakeLists.txt and Doxyfile editing
        """
        # The value of 'directories' key will be used if it already exists;
        # otherwise fill in the value from the positional argument
        kwargs.setdefault("directories", directories)

        __ARGUMENTS = {"authors": self.authors_set,
                       "directories": self.directories_set,
                       "language": self.language_set,
                       "license": self.license_set,
                       "quiet": self.quiet_set}
        self.__config = dict()
        self.__languages = frozenset(("c", "cpp"))
        self.__licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))
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
        'authors' must be an iterable type containing 'str'(s).
        This member function is called by the constructor by default.

        Sets the single author to be the GECOS or name field of current
        logged-in user if 'authors' is left as default or 'None'.
        """
        if None == authors:
            self.__config["authors"] = set()
            self.author_add(SkaffConfig.author_fetch())
            return

        if not isinstance(authors, collections.Iterable):
            raise ValueError("'authors' argument must be iterable")

        if isinstance(authors, str):
            raise ValueError(("'authors' argument must be an iterable "
                             "containing 'str' type"))

        if 0 == len(authors):
            raise ValueError("'authors' argument must not be empty")

        if not all(isinstance(author, str) for author in authors):
            raise ValueError("'authors' argument must contain 'str' type")

        if not all(author.isprintable() for author in authors):
            raise ValueError("'authors' argument must contain valid names")

        self.__config["authors"] = set()

        for author in authors:
            self.author_add(author)

    def author_add(self, author):
        """
        Adds 'author' to the internal 'database' if the name does not exist;
        otherwise do nothing.
        """
        if not isinstance(author, str):
            raise ValueError("'author' argument must be 'str' type")

        if 0 == len(author):
            raise ValueError("'author' argument must not be empty")

        if not author.isprintable():
            raise ValueError("'author' argument must be a valid name")

        self.__config["authors"].add(author)

    def author_discard(self, author):
        """
        Discards 'author' from the internal 'database' if the name exists;
        otherwise do nothing.
        """
        if not isinstance(author, str):
            raise ValueError("'author' argument must be 'str' type")

        if 0 == len(author):
            raise ValueError("'author' argument must not be empty")

        if not author.isprintable():
            raise ValueError("'author' argument must be a valid name")

        self.__config["authors"].discard(author)

    def authors_get(self):
        """
        Gets the author(s) of the project(s).
        """
        return sorted(self.__config["authors"])

    @staticmethod
    def author_fetch():
        """
        Gets the current logged-in username from GECOS or name field.
        This member function is called by the constructor by default.

        Raises RuntimeError if both attempts fail.

        Note this 'classmethod' may be automatically called from 'authors_get'
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
        Sets the name(s) of the outputting project-directory(ies).
        'directories' must be an iterable type containing 'str'(s).
        This member function is called by the constructor by default.

        'directories' argument must be of 'collections.Iterable' type
        containing instance of 'str'(s).
        """
        if not isinstance(directories, collections.Iterable):
            raise ValueError("'directories' argument must be iterable")

        if isinstance(directories, str):
            raise ValueError(("'directories' argument must be an iterable "
                             "containing 'str' type"))

        if 0 == len(directories):
            raise ValueError("'directories' argument must not be empty")

        if not all(isinstance(directory, str) for directory in directories):
            raise ValueError("'directories' argument must contain 'str' type")

        if not all(directory.isprintable() for directory in directories):
            raise ValueError(("'directories' argument must contain "
                             "valid file names"))

        self.__config["directories"] = set()

        for directory in directories:
            self.directory_add(directory)

    def directory_add(self, directory):
        """
        Adds 'directory' to the internal 'database' if the name does not exist;
        otherwise do nothing.
        """
        if not isinstance(directory, str):
            raise ValueError("'directory' argument must be 'str' type")

        if 0 == len(directory):
            raise ValueError("'directory' argument must not be empty")

        if not directory.isprintable():
            raise ValueError("'directory' argument must be a valid file name")

        self.__config["directories"].add(directory)

    def directory_discard(self, directory):
        """
        Discards 'directory' from the internal 'database' if the name exists;
        otherwise do nothing.
        """
        if not isinstance(directory, str):
            raise ValueError("'directory' argument must be 'str' type")

        if 0 == len(directory):
            raise ValueError("'directory' argument must not be empty")

        if not directory.isprintable():
            raise ValueError("'directory' argument must be a valid file name")

        self.__config["directories"].discard(directory)

    def directories_get(self):
        """
        Gets the name(s) of the outputting project-directory(ies).
        """
        return sorted(self.__config["directories"])

    def language_set(self, language=None):
        """
        Sets the major programming language used.
        Defaults to 'c' language if left as empty or 'None'.
        This member function is called by the constructor by default.

        'language' argument must be the ones listed in 'languages_list'.
        """
        languages = self.languages_list()

        if None == language:
            self.__config["language"] = "c"
            return

        if language not in languages:
            raise ValueError(("'language' choice must be one of the following:"
                              " "
                              ", ".join(languages)))

        self.__config["language"] = language

    def language_get(self):
        """
        Gets the major programming language used.
        """
        return self.__config["language"]

    def languages_list(self):
        """
        Lists the supported primary programming languages.
        By default they are the following:
        {"c", "cpp"}.
        """
        return sorted(self.__languages)

    def license_set(self, license=None):
        """
        Sets the type of license.
        Defaults to 'bsd2' license if left as empty or 'None'.
        This member function is called by the constructor by default.

        'license' argument must be the ones listed in 'licenses_list'.
        """
        licenses = self.licenses_list()

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

    def licenses_list(self):
        """
        Lists the supported licenses.
        By default they are the following:
        {"bsd2", "bsd3", "gpl2", "gpl3", "mit"}.
        """
        return sorted(self.__licenses)

    def quiet_set(self, quiet=None):
        """
        Sets whether there is interactive CMakeLists.txt and Doxyfile editing.
        'True' to turn off the interactive editing.
        Defaults to 'False' if left as empty or 'None'.
        This member function is called by the constructor by default.

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

    def subdirectories_set(self, subdirectories):
        """
        Sets the name(s) of the subdirectory(ies) within the project(s)' base
        directory(ies).
        This member function is called by the constructor by default.

        'subdirectories' argument must be of 'collections.Iterable' type
        containing instance of 'str'(s).
        """
        pass

    def subdirectory_add(self, subdirectory):
        """
        Adds 'subdirectory' to the internal 'database' if the name does not
        exist; otherwise do nothing.
        """
        pass

    def subdirectory_discard(self, subdirectory):
        """
        Discards 'subdirectory' from the internal 'database' if the name
        exists; otherwise do nothing.
        """
        pass

    def subdirectories_get(self):
        """
        Gets the name(s) of the subdirectory(ies) within the project(s)' base
        directory(ies).
        """
        pass

    def _load(self, **kwargs):
        """
        """
        pass

    def _save(self, **kwargs):
        """
        """
        pass

# --------------------------------- CLASSES -----------------------------------
