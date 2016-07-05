#!/usr/bin/env python3

"""
Custom configuration type definition used for the 'core' skaff module.
"""

# --------------------------------- MODULES -----------------------------------
import collections
import copy
import glob
import os
import pwd
import shutil

from datetime import datetime
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class SkaffConfig:
    """
    Configuration type used for the argument of 'skaff' function.
    """
    # 'languages', 'licenses', and 'subdirectories' can only be determined
    # for a given 'paths' attribute since all the mutators associated with
    # the former three directly or indirectly call their corresponding _*probe
    # methods, which need info about 'paths'.
    #
    # Similarly, 'authors', 'language', 'license', and 'quiet' are associated
    # with a list of 'directories'.
    #
    # NOTE: 'languages', 'licenses', and 'templates' attributes may be dropped
    # without actually affecting the behavior of this class since mutators for
    # all three ('language_set', 'license_set', 'templates_set') automatically
    # call 'languages_probe' and 'licenses_probe' 'templates_probe'
    # respectively to enforce the dependency.
    # However, for verbosity and most importantly completeness they are listed
    # here as well: the only drawback I can think of is THREE MORE REDUNDANT
    # calls at object construction time.
    #
    #
    # A dependency graph for the first relation stated above is:
    #
    #                                +-----+
    #                                |paths|
    #                                +-----+
    #                                   ^
    #                                   |
    #                    +---------+--------+--------------+
    #                    |languages|licenses|subdirectories|
    #                    +---------+--------+--------------+
    #                         ^                    ^
    #                         |                    |
    #                         +--------------------+
    #                         |     templates      |
    #                         +--------------------+
    #
    # A dependency graph for the second is:
    #
    #                              +-----------+
    #                              |directories|
    #                              +-----------+
    #                                   ^
    #                                   |
    #                      +-------+--------+-------+-----+
    #                      |authors|language|license|quiet|
    #                      +-------+--------+-------+-----+
    #
    __ATTRIBUTES = ("paths",
                    "languages", "licenses", "subdirectories",
                    "directories",
                    "authors", "language", "license", "quiet")
    __LANGUAGES = frozenset(("c", "cpp"))
    __LICENSE_FORMATS = frozenset((".txt", ".md"))
    __LICENSES = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))

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
                    must be chosen from the 'languages_list' listing

        'license': type of license;
                    must be chosen from the 'licenses_list' listing

        'paths': paths containing configuration, template, and license files

        'quiet': no interactive CMakeLists.txt and Doxyfile editing

        'subdirectories': set of name(s) for the subdirectory(ies)
        within the project(s)' base directory(ies)
        """
        __METHODS = (self.paths_set,
                     self.languages_probe,
                     self.licenses_probe,
                     self.subdirectories_set,
                     # End of 1st dependency and begin of 2nd dependency
                     self.directories_set,
                     self.authors_set,
                     self.language_set,
                     self.license_set,
                     self.quiet_set)

        # The value of 'directories' key will be used if it already exists;
        # otherwise fill in the value from the positional argument
        kwargs.setdefault("directories", directories)

        # Mapping between valid attributes(arguments) and corresponding methods
        relation = zip(SkaffConfig.__ATTRIBUTES, __METHODS)
        __ARGUMENTS = collections.OrderedDict(relation)

        # The actual internal per-instance mapping between
        # attributes(arguments) and corresponding values
        self.__config = dict.fromkeys(SkaffConfig.__ATTRIBUTES)

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
            raise TypeError("'authors' argument must be iterable")

        if isinstance(authors, str):
            raise TypeError(("'authors' argument must be an iterable "
                             "containing 'str' type"))

        if 0 == len(authors):
            raise ValueError("'authors' argument must not be empty")

        self.__config["authors"] = set()

        for author in authors:
            self.author_add(author)

    def author_add(self, author):
        """
        Adds 'author' to the internal 'database' if the name does not exist;
        otherwise do nothing.
        """
        if not isinstance(author, str):
            raise TypeError("'author' argument must be 'str' type")

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
            raise TypeError("'author' argument must be 'str' type")

        if 0 == len(author):
            raise ValueError("'author' argument must not be empty")

        if not author.isprintable():
            raise ValueError("'author' argument must be a valid name")

        self.__config["authors"].discard(author)

    def authors_get(self):
        """
        Gets a generator containing author(s) for the project(s).
        """
        authors = sorted(self.__config["authors"])
        yield from (author for author in authors)

    @staticmethod
    def author_fetch():
        """
        Gets the current logged-in username from GECOS or name field.
        This member function is called by the constructor by default.

        Raises RuntimeError if both attempts fail.

        Note this 'staticmethod' may be automatically called from 'authors_get'
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

    @staticmethod
    def basepath_fetch():
        """
        Returns the base directory name containing the skaff 'config' module.

        The extra 'os.path.abspath' invocation is to suppress relative path
        output; result includes a trailing path separator.
        """
        return os.path.dirname(os.path.abspath(__file__)) + os.sep

    def create(self, *args):
        """
        Supported arguments:

        'tree':
        'license':
        'template':
        """
        # An 'OrderedDict' is required for the default case:
        # the 'tree' made of 'directories' and 'subdirectories' need to be
        # created before the selected license and template files
        options = ("tree", "license", "template")
        methods = (None, None, None)
        actions = collections.OrderedDict(zip(options, methods))

        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("'args' must contain 'str' types")

        if not all(arg in options for arg in args):
            raise ValueError(("'args' must be selected from: "
                              ", ".join(options)))

        # Make 'args' variable "point to" the tuple object 'options' variable
        # "points to" if 'args' is left as empty
        if 0 == len(args):
            args = options

        for arg in args:
            actions[arg]()

    def directories_set(self, directories=None):
        """
        Sets the name(s) of the outputting project-directory(ies).
        Platform-dependent path separator will be appended if missing.
        This member function is called by the constructor by default.

        'directories' argument must be of 'collections.Iterable' type
        containing instance of 'str'(s).
        """
        if not isinstance(directories, collections.Iterable):
            raise TypeError("'directories' argument must be iterable")

        if isinstance(directories, str):
            raise TypeError(("'directories' argument must be an iterable "
                             "containing 'str' type"))

        if 0 == len(directories):
            raise ValueError("'directories' argument must not be empty")

        self.__config["directories"] = set()

        for directory in directories:
            self.directory_add(directory)

    def directory_add(self, directory):
        """
        Adds 'directory' to the internal 'database' if the name does not exist;
        otherwise do nothing.
        Platform-dependent path separator will be appended if missing.
        """
        if not isinstance(directory, str):
            raise TypeError("'directory' argument must be 'str' type")

        if 0 == len(directory):
            raise ValueError("'directory' argument must not be empty")

        if not directory.isprintable():
            raise ValueError("'directory' argument must be a valid file name")

        if not directory.endswith(os.sep):
            directory += os.sep

        self.__config["directories"].add(directory)

    def directory_discard(self, directory):
        """
        Discards 'directory' from the internal 'database' if the name exists;
        otherwise do nothing.
        Platform-dependent path separator will be appended if missing.
        """
        if not isinstance(directory, str):
            raise TypeError("'directory' argument must be 'str' type")

        if 0 == len(directory):
            raise ValueError("'directory' argument must not be empty")

        if not directory.isprintable():
            raise ValueError("'directory' argument must be a valid file name")

        if not directory.endswith(os.sep):
            directory += os.sep

        self.__config["directories"].discard(directory)

    def directories_get(self):
        """
        Gets a generator containing name(s) for the outputting
        project-directory(ies).
        """
        directories = sorted(self.__config["directories"])
        yield from (directory for directory in directories)

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

    @staticmethod
    def languages_fetch():
        """
        Gets a list containing the supported programming languages BY DEFAULT.
        User-defined programming languages are not shown.
        """
        return sorted(SkaffConfig.__LANGUAGES)

    def languages_list(self):
        """
        Gets a generator containing the supported programming languages.

        By default they are the following:
        {"c", "cpp"}.
        """
        languages = sorted(SkaffConfig.__LANGUAGES)
        yield from (language for language in languages)

    def languages_probe(self):
        """
        This member function is called by the constructor by default.
        """
        pass

    def license_set(self, license=None):
        """
        Sets the type of license used.
        Defaults to 'bsd2' license if left as empty or 'None'.
        This member function is called by the constructor by default.

        'license' argument must be the ones listed in 'licenses_list'.
        """
        # Ensure all the stock licenses do indeed exist
        self.licenses_validate()
        # Also probes the user path for possible custom licenses
        self.licenses_probe()
        licenses = self.licenses_list()

        if None == license:
            self.__config["license"] = "bsd2"
            return

        if license not in licenses:
            raise ValueError(("'license' choice must be one of the following: "
                              ", ".join(licenses)))

        self.__config["license"] = license

    def license_get(self, fullname=False):
        """
        Gets the type of license used if 'fullname' argument is set to 'False';
        otherwise gets a list containing current selected license with fully
        qualified paths and file extensions attached.

        NOTE: The paths and file extensions associated with the current license
        are governed by the rules specified in the docstrings of 'paths_set'
        and 'licenses_list'.
        """
        user_license_path = self.paths_get("license")
        system_license_path = (SkaffConfig.basepath_fetch() +
                               "config" + os.sep + "license" + os.sep)
        license_results = list()

        if not fullname:
            return self.__config["license"]

        for extension in SkaffConfig.__LICENSE_FORMATS:
            user_license_file_name = (user_license_path +
                                      self.__config["license"] + extension)
            sys_license_file_name = (system_license_path +
                                     self.__config["license"] + extension)
            if os.path.isfile(user_license_file_name):
                license_results.append(user_license_file_name)
            elif os.path.isfile(sys_license_file_name):
                license_results.append(sys_license_file_name)
            else:
                raise FileNotFoundError(("License file '{}' not found".format(
                    self.__config["license"])))

        return license_results

    @staticmethod
    def licenses_fetch():
        """
        Gets a list containing the supported licenses BY DEFAULT.
        User-defined licenses are not shown.
        """
        return sorted(SkaffConfig.__LICENSES)

    def licenses_list(self, fullname=False):
        """
        Gets a generator containing the supported licenses with or without
        paths and file exntensions, depending on whether 'fullname' is enabled.
        For new licenses added in the license path (refer to docstrings for
        'paths_set' mutator member function for details), remember to call
        'licenses_probe' mutator member function to actually add them to the
        internal database; otherwise they would not be listed.

        NOTE: For overridden licenses (licenses with the same name as the
        stock licenses but appear in the license path set by 'license_set'),
        this generator will only reflect the difference when 'fullname'
        argument is switched to 'True'.
        For exmaple, with license path set to

        "$HOME/.config/skaff/license/"

        and a custom 'bsd2' license is set up as:

        "$HOME/.config/skaff/license/bsd2.txt"

        "$HOME/.config/skaff/license/bsd2.md"

        then a licenses_list() invocation would only produce the SAME DEFAULT
        result as shown at the BOTTOM; only licenses_list(True) will generate
        fully qualified results like:

        "$HOME/.config/skaff/license/bsd2.txt"

        "$HOME/.config/skaff/license/bsd2.md"

        (Note the rest default stock licenses are left untouched;
        the stock bsd2 license in the system path would not be shown
        since it is overridden)

        "/usr/lib/python3/dist-packages/skaff/config/license/bsd3.txt"

        "/usr/lib/python3/dist-packages/skaff/config/license/bsd3.md"

        ...

        By default they are the following:
        {"bsd2", "bsd3", "gpl2", "gpl3", "mit"}.
        """
        licenses = sorted(self.__config["licenses"])
        user_license_path = self.paths_get("license")
        system_license_path = (SkaffConfig.basepath_fetch() +
                               "config" + os.sep + "license" + os.sep)

        if not fullname:
            yield from (license for license in licenses)
        else:
            for license in licenses:
                for ext in SkaffConfig.__LICENSE_FORMATS:
                    user_license_file_name = user_license_path + license + ext
                    sys_license_file_name = system_license_path + license + ext
                    if os.path.isfile(user_license_file_name):
                        yield user_license_file_name
                    elif os.path.isfile(sys_license_file_name):
                        yield sys_license_file_name
                    else:
                        raise FileNotFoundError(("The corresponding files for "
                                                 "'{}' license is not found"
                                                 .format(license)))

    def licenses_probe(self):
        """
        Probes the 'license' path set by the 'paths_set' member function for
        new licenses and add them to the internal 'database' to be returned
        by 'licenses_list' member function.

        NOTE: normally this member function does not need to be called manually
        (if some new license files get copied to the 'license' path, for
        example) since 'license_set' automatically calls this member function;
        unless you just want to add those custom licenses to the internal
        'database' WITHOUT switching the CURRENT license selected.
        """
        # Reset the internal licenses database
        self.__config["licenses"] = set(SkaffConfig.__LICENSES)
        user_license_path = self.paths_get("license")
        # Temporary dictionary used for comparison between licenses
        # named with ".txt" and ".md" extension
        license_extensions = SkaffConfig.__LICENSE_FORMATS
        temp_license_dict = {key: set() for key in license_extensions}
        normalize_funcs = (os.path.basename, os.path.splitext, lambda x: x[0])

        if not os.path.isdir(user_license_path):
            return

        for file_ext in temp_license_dict.keys():
            for user_license in glob.iglob(user_license_path + "*" + file_ext):
                # Remove the file extension and path
                for func in normalize_funcs:
                    user_license = func(user_license)
                temp_license_dict[file_ext].add(os.path.basename(user_license))

        if temp_license_dict[".txt"] != temp_license_dict[".md"]:
            raise FileNotFoundError(("The number of license files end with "
                                     "those file extensions must equal; "
                                     "there must be a file with same name for "
                                     "each of the following file extension: "
                                     ", ".join(temp_license_dict.keys())))

        self.__config["licenses"] |= temp_license_dict[".txt"]
        # rootDir = '.'
        # for dirName, subdirList, fileList in os.walk(rootDir):
        #     print('Found directory: %s' % dirName)
        #     for fname in fileList:
        #         print('\t%s' % fname)

    def licenses_validate(self):
        """
        Validates all the stock licenses distributed along with the 'skaff'
        program (does not change any internal states).
        By default they reside under license subdirectory of 'system' config
        path, which is not modifiable (see docstring of 'paths_set'):
        "/usr/lib/python3/dist-packages/skaff/config/license/"
        """
        # The 'system' paths are hard-coded and cannot be changed freely;
        # in contrast to the 'user' paths set through the 'paths_set'
        # mutator member function interface
        system_config_path = (SkaffConfig.basepath_fetch() +
                              "config" + os.sep)
        system_license_path = system_config_path + "license" + os.sep
        # system_template_path = system_config_path + "template" + os.sep
        file_extensions = (".txt", ".md")

        for system_path in (system_config_path, system_license_path):
            if not os.path.isdir(system_path):
                raise FileNotFoundError("The system path: '{}' does not exist"
                                        .format(system_path))

        for license in SkaffConfig.__LICENSES:
            for file_ext in file_extensions:
                license_file = system_license_path + license + file_ext
                if not os.path.isfile(license_file):
                    raise FileNotFoundError(("The stock version of license "
                                             "file: '{}' does not exist"
                                             .format(license_file)))

    def paths_set(self, **kwargs):
        """
        Sets the paths containing configuration, template, and license files.
        This member function is called by the constructor by default.

        NOTE: the paths containing configuration, template, and license files
        specified here will take precedence over files with identical name in
        the 'system' path.
        For example, if there is a file named 'bsd.txt' in the default path of
        license files:
        "$HOME/.config/skaff/license/bsd.txt"
        then the content within that file will be used instead of the supplied
        stock version
        "/usr/lib/python3/dist-packages/skaff/config/license/bsd.txt"
        when you create a project using 'bsd' license; same goes for templates.
        You can add new configuration, template, and licenses in this path and
        it will be discovered by corresponding _*probe member functions, which
        are called by the constructor by default.

        Supported keyword arguments:

        'config': path containing 'skaff.json' configuration file.
        Default is:
        "$HOME/.config/skaff/"

        'license': path containing license files to be copied to the
        directories specified in 'directories_set' or 'directory_add'.
        Default is:
        "$HOME/.config/skaff/license/"

        'template': path containing template files to be copied to the
        directories specified in 'directories_set', 'directory_add',
        'subdirectories_set', or 'subdirectory_add'.
        Default is:
        "$HOME/.config/skaff/template/"
        """
        keys = ("config", "license", "template")
        items = kwargs.items()
        user_config = os.path.expanduser("~") + os.sep + ".config" + os.sep +\
            "skaff" + os.sep
        user_template = user_config + "template" + os.sep
        user_license = user_config + "license" + os.sep

        if not all(key in keys and isinstance(val, str) for key, val in items):
            raise ValueError(("values of 'kwargs' must be of 'str' type and "
                              "keys must be one of the following keywords: "
                              ", ".join(keys)))

        kwargs.setdefault("config", user_config)
        kwargs.setdefault("template", user_template)
        kwargs.setdefault("license", user_license)

        self.__config["paths"] = dict()
        self.__config["paths"]["config"] = kwargs["config"]
        self.__config["paths"]["license"] = kwargs["license"]
        self.__config["paths"]["template"] = kwargs["template"]

    def paths_get(self, *args):
        """
        Gets the paths containing configuration, template, and license files.
        Accepted arguments are strings: 'config', 'license' and 'template'.

        If called without any actual argument, returns a deep copy of the
        internal dictionary containing all the stored key-value pairs.

        If called with multiple arguments, a list with corresponding results
        will be returned.
        """
        result_paths = list()

        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("'args' must contain 'str' types")

        if 0 == len(args):
            return copy.deepcopy(self.__config["paths"])

        if 1 == len(args):
            return self.__config["paths"][args[0]]

        for arg in args:
            result_paths.append(self.__config["paths"][arg])

    def quiet_set(self, quiet=None):
        """
        Sets whether there is interactive CMakeLists.txt and Doxyfile editing.
        'True' to turn off the interactive editing.
        Defaults to 'True' if left as empty or 'None'.
        This member function is called by the constructor by default.

        'quiet' argument must be of 'bool' type.
        """
        if None == quiet:
            self.__config["quiet"] = True
            return

        if not isinstance(quiet, bool):
            raise TypeError("'quiet' must be of 'bool' type")

        self.__config["quiet"] = quiet

    def quiet_get(self):
        """
        Gets whether there is interactive CMakeLists.txt and Doxyfile editing.
        """
        return self.__config["quiet"]

    def subdirectories_set(self, subdirectories=None):
        """
        Sets the name(s) of the subdirectory(ies) within the project(s)' base
        directory(ies).
        Defaults to
        {"build", "coccinelle", "doc", "examples", "img", "src", "tests"}
        if left as empty or 'None'.
        Platform-dependent path separator will be appended if missing.
        This member function is called by the constructor by default.

        'subdirectories' argument must be of 'collections.Iterable' type
        containing instance of 'str'(s).
        """
        if None == subdirectories:
            self.__config["subdirectories"] = set((
                "build",
                "coccinelle",
                "doc",
                "examples",
                "img",
                "src",
                "tests"
            ))
            return

        if not isinstance(subdirectories, collections.Iterable):
            raise TypeError("'subdirectories' argument must be iterable")

        if isinstance(subdirectories, str):
            raise TypeError(("'subdirectories' argument must be an iterable "
                             "containing 'str' type"))

        if 0 == len(subdirectories):
            raise ValueError("'subdirectories' argument must not be empty")

        self.__config["subdirectories"] = set()

        for directory in subdirectories:
            self.subdirectory_add(directory)

    def subdirectory_add(self, subdirectory):
        """
        Adds 'subdirectory' to the internal 'database' if the name does not
        exist; otherwise do nothing.
        Platform-dependent path separator will be appended if missing.
        """
        if not isinstance(subdirectory, str):
            raise TypeError("'subdirectory' argument must be 'str' type")

        if 0 == len(subdirectory):
            raise ValueError("'subdirectory' argument must not be empty")

        if not subdirectory.isprintable():
            raise ValueError(("'subdirectory' argument must be "
                              "a valid file name"))

        if not subdirectory.endswith(os.sep):
            subdirectory += os.sep

        self.__config["subdirectories"].add(subdirectory)

    def subdirectory_discard(self, subdirectory):
        """
        Discards 'subdirectory' from the internal 'database' if the name
        exists; otherwise do nothing.
        Platform-dependent path separator will be appended if missing.
        """
        if not isinstance(subdirectory, str):
            raise TypeError("'subdirectory' argument must be 'str' type")

        if 0 == len(subdirectory):
            raise ValueError("'subdirectory' argument must not be empty")

        if not subdirectory.isprintable():
            raise ValueError(("'subdirectory' argument must be "
                             "a valid file name"))

        if not subdirectory.endswith(os.sep):
            subdirectory += os.sep

        self.__config["subdirectories"].discard(subdirectory)

    def subdirectories_get(self):
        """
        Gets a generator containing name(s) of the subdirectory(ies) within the
        project(s)' base directory(ies).
        """
        subdirectories = sorted(self.__config["subdirectories"])
        yield from (subdirectory for subdirectory in subdirectories)

    def templates_set(self, templates=None):
        """
        """
        pass

    def template_add(self, template):
        """
        """
        pass

    def template_discard(self, template):
        """
        """
        pass

    def templates_get(self, fullname=False):
        """
        """
        pass

    def templates_probe(self):
        """
        """
        pass

    def _license_sign(self, directory, config):
        """
        Copies the license text (ends with ".txt" extension) chosen by authors
        to the 'directories', signs it with authors and current year prepended
        if applicable; 'directories' must already exist.

        Note only licenses in {"bsd2", "bsd3", "mit"} will be signed by names
        in authors.
        """
        copyright_line = "Copyright (c) {year}, {authors}\n".format(
            year=datetime.now().year,
            authors=", ".join(self.authors_get())
        )
        # Note "figuring out where the source license resides" may belong to
        # the responsibility of 'SkaffConfig' class; this responsibiltiy will
        # be moved to 'SkaffConfig' after "json-parsing" functionality is
        # implemented.
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

    def _load(self, *args):
        """
        """
        pass

    def _save(self, *args):
        """
        """
        pass
# --------------------------------- CLASSES -----------------------------------
