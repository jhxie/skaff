#!/usr/bin/env python3

"""
Unit testing suite for config module.
"""
# --------------------------------- MODULES -----------------------------------
import collections
import os
import pwd
import unittest

from skaff import SkaffConfig
from tempfile import TemporaryDirectory
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class TestConfig(unittest.TestCase):
    """
    Unit testing suite for 'config' module.
    """
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        if not self.tmp_dir.name.endswith(os.sep):
            self.tmp_dir.name += os.sep
        # NOTE: the 'directories' argument needs to be an iterable;
        # a tuple (denoted by an extra comma inside the parentheses) is used.
        self.config = SkaffConfig((self.tmp_dir.name,))

    def tearDown(self):
        # No need to invoke 'directory_discard' since for each test member
        # function a new 'SkaffConfig' instance is created.
        self.tmp_dir.cleanup()

    def test_authors_set(self):
        # The branch where 'authors' is 'None' is tested in 'test_author_fetch'
        # member function, so it is skipped here
        authors = ["Andrew Grove", "An Wang", lambda x: not x]

        # Fail due to non-iterable type
        with self.assertRaises(TypeError):
            self.config.authors_set(authors[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(TypeError):
            self.config.authors_set(authors[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.authors_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(TypeError):
            self.config.authors_set(authors)

        authors[-1] = "\t"
        # Fail due to the existence of non-printable string
        with self.assertRaises(ValueError):
            self.config.authors_set(authors)

        del authors[-1]
        self.config.authors_set(authors)
        self.assertCountEqual(authors, self.config.authors_get())

    def test_author_add(self):
        # This "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        author_added = "Karl Pearson"
        counter = None

        # Fail due to wrong type for the 'author' argument
        with self.assertRaises(TypeError):
            self.config.author_add(None)

        # Fail because the 'author' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.author_add(str())

        # Fail because the 'author' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.author_add("\t")

        for _ in range(add_count):
            self.config.author_add(author_added)
        # Success if 'author_add' actually added the specified 'author'
        self.assertIn(author_added, self.config.authors_get())

        counter = collections.Counter(self.config.authors_get())
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertEqual(1, counter[author_added])

    def test_author_discard(self):
        # Again, this "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        author_discarded = "Lewis Terman"

        # Fail due to wrong type for the 'author' argument
        with self.assertRaises(TypeError):
            self.config.author_discard(None)

        # Fail because the 'author' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.author_discard(str())

        # Fail because the 'author' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.author_discard("\t")

        for _ in range(add_count):
            self.config.author_add(author_discarded)
        self.config.author_discard(author_discarded)
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertNotIn(author_discarded, self.config.authors_get())

    def test_authors_get(self):
        authors = ("Pratt", "Whitney")
        get_result = None

        self.config.authors_set(authors)
        get_result = self.config.authors_get()
        self.assertCountEqual(authors, get_result)

    def test_author_fetch(self):
        # Get system password database record based on current user UID
        pw_record = pwd.getpwuid(os.getuid())

        # '_author_get()' must return identical term if GECOS field is defined
        if pw_record.pw_gecos:
            self.assertEqual(SkaffConfig.author_fetch(), pw_record.pw_gecos)
        # Otherwise it must matches the current user's login name
        elif pw_record.pw_name:
            self.assertEqual(SkaffConfig.author_fetch(), pw_record.pw_name)
        # If none of the above works, 'RuntimeError' is raised
        else:
            with self.assertRaises(RuntimeError):
                SkaffConfig.author_fetch()

    def test_basepath_fetch(self):
        basepath = SkaffConfig.basepath_fetch()

        self.assertTrue(os.path.isdir(basepath))
        self.assertTrue(os.path.isabs(basepath))

    def test_directories_set(self):
        # Identical to 'test_authors_set' because the similarity between
        # the 2 mutator member functions; may be expanded later on if new
        # checking branches are added to 'directories_set'
        directories = ["Apollo" + os.sep, "Spirit" + os.sep, lambda x: not x]

        # Fail due to non-iterable type
        with self.assertRaises(TypeError):
            self.config.directories_set(directories[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(TypeError):
            self.config.directories_set(directories[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.directories_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(TypeError):
            self.config.directories_set(directories)

        directories[-1] = "\t"
        # Fail due to the existence of non-printable string
        with self.assertRaises(ValueError):
            self.config.directories_set(directories)

        # Success
        del directories[-1]
        self.config.directories_set(directories)
        self.assertCountEqual(directories, self.config.directories_get())

    def test_directory_add(self):
        # Again, identical to 'test_author_add'.
        # This "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        directory_added = "Android"
        counter = None

        # Fail due to wrong type for the 'directory' argument
        with self.assertRaises(TypeError):
            self.config.directory_add(None)

        # Fail because the 'directory' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.directory_add(str())

        # Fail because the 'directory' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.directory_add("\t")

        for _ in range(add_count):
            self.config.directory_add(directory_added)
        # Success if 'directory_add' actually added the specified 'directory'
        self.assertIn(directory_added + os.sep, self.config.directories_get())

        counter = collections.Counter(self.config.directories_get())
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertEqual(1, counter[directory_added + os.sep])

    def test_directory_discard(self):
        # Again, identical to 'test_author_discard'.
        # This "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        directory_discarded = "Symbian"

        # Fail due to wrong type for the 'author' argument
        with self.assertRaises(TypeError):
            self.config.directory_discard(None)

        # Fail because the 'author' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.directory_discard(str())

        # Fail because the 'author' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.directory_discard("\t")

        # The path separator will be automatically added in both
        # 'directory_add' and 'directory_discard' member functions
        for _ in range(add_count):
            self.config.directory_add(directory_discarded)
        self.config.directory_discard(directory_discarded)
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertNotIn(directory_discarded, self.config.directories_get())
        self.assertNotIn(directory_discarded + os.sep,
                         self.config.directories_get())

    def test_directories_get(self):
        # Test directory names with non-ascii characters
        directories = ["Αντικύθηρα" + os.sep, "Ουροβόρος όφις" + os.sep]
        get_result = None

        self.config.directories_set(directories)
        get_result = self.config.directories_get()
        self.assertCountEqual(directories, get_result)

    def test_language_set(self):
        language = "Svenska"
        languages = self.config.languages_list()

        # Whatever the default programming language is, it must conform to its
        # own invarients: the language set automatically must belong to the
        # listing of supported languages generated by the class itself.
        self.config.language_set(None)
        self.assertIn(self.config.language_get(), languages)

        self.assertNotIn(language, languages)
        with self.assertRaises(ValueError):
            self.config.language_set(language)

    def test_language_get(self):
        # Every language specified in the listing should work.
        for language in self.config.languages_list():
            self.config.language_set(language)
            self.assertEqual(language, self.config.language_get())

    def test_languages_probe(self):
        pass

    def test_license_set(self):
        # Identical to 'test_language_set' due to the similarity between
        # 'language_set' and 'license_set' mutator functions.
        license = "proprietary"
        licenses = self.config.licenses_list()

        self.config.license_set(None)
        self.assertIn(self.config.license_get(), licenses)

        self.assertNotIn(license, licenses)
        with self.assertRaises(ValueError):
            self.config.license_set(license)

    def test_license_get(self):
        bsd2_text = ("Random Empty Replacement Text")
        bsd2_markdown = (
            "Licensed under the BSD 2 Clause License.  \n"
            "Distributed under the BSD 2 Clause License.  \n\n")
        bsd2_text_name = self.tmp_dir.name + "bsd2.txt"
        bsd2_markdown_name = self.tmp_dir.name + "bsd2.md"
        normalize_funcs = (os.path.basename, os.path.splitext, lambda x: x[0])
        system_licenses = None
        user_licenses = None

        # Every license specified in the listing should work.
        for license in self.config.licenses_list():
            self.config.license_set(license)
            self.assertEqual(license, self.config.license_get())

        # The following tests abide by the similar test patern used in
        # 'test_license_list'; but slightly simpler.
        # Revert to the default license
        self.config.license_set()
        system_licenses = self.config.license_get(fullname=True)

        with open(bsd2_text_name, "w") as license_text:
            license_text.write(bsd2_text)

        with open(bsd2_markdown_name, "w") as license_markdown:
            license_markdown.write(bsd2_markdown)

        # Add the overriden 'bsd2' license to the internal database
        self.config.paths_set(license=self.tmp_dir.name)
        self.config.licenses_probe()
        user_licenses = self.config.license_get(fullname=True)

        # Success if two versions of qualified licenses differ;
        # should be the case if 'bsd2' license is successfully overriden
        self.assertNotEqual(system_licenses, user_licenses)

        # Success if the fully qualified version of the licenses are equivalent
        # to each other after removing paths and file extensions
        for licenses in (system_licenses, user_licenses):
            for index, license in enumerate(licenses):
                for func in normalize_funcs:
                    licenses[index] = func(license)

        self.assertEqual(system_licenses, user_licenses)

        os.remove(bsd2_text_name)
        os.remove(bsd2_markdown_name)

    def test_licenses_list(self):
        licenses = set(self.config.licenses_list(fullname=False))
        qualified_licenses = set(self.config.licenses_list(fullname=True))
        result_licenses = set()
        bsd2_text = ("Random Empty Replacement Text")
        bsd2_markdown = (
            "Licensed under the BSD 2 Clause License.  \n"
            "Distributed under the BSD 2 Clause License.  \n\n")
        bsd2_text_name = self.tmp_dir.name + "bsd2.txt"
        bsd2_markdown_name = self.tmp_dir.name + "bsd2.md"
        system_config_path = (SkaffConfig.basepath_fetch() + "config" + os.sep)
        system_license_path = system_config_path + "license" + os.sep

        # Similar to what is done in 'test_licenses_probe',
        # sets the 'user' 'license' path to the temporary directory
        # so all the licenses created in this test case would be
        # automatically removed upon completion (by the 'tearDown')
        self.config.paths_set(license=self.tmp_dir.name)

        # The number of qualified version of license
        # (licenses with fully qualified path and extension) is equal to
        # the number of file exntension supported per license * actual number
        # of licenses supported
        # For example, for the current version 1.0, the supported file formats
        # for each license are ".txt" and ".md" (refer to the __LICNESE_FORMATS
        # private class attribute for details), if the fully qualified version
        # of filenames are needed, then for each file both ".txt" version of
        # the license and ".md" version of the license will be returned.
        #
        # Therefore the length of the 'qualified_licenses' is equal to the
        # number of file formats for each license (".txt", ".md") times the
        # actual number of license ('licenses' variable here).
        self.assertEqual(len(licenses) * 2, len(qualified_licenses))

        # Success if the fully qualified version of the licenses are equivalent
        # to the originals after removing path and extension.
        for license in qualified_licenses:
            for func in (os.path.basename, os.path.splitext, lambda x: x[0]):
                license = func(license)
            result_licenses.add(license)

        self.assertEqual(licenses, result_licenses)

        # Both text and markdown format of the overriden license need to
        # present; otherwise 'licenses_probe' will fail
        with open(bsd2_text_name, "w") as license_text:
            license_text.write(bsd2_text)

        with open(bsd2_markdown_name, "w") as license_markdown:
            license_markdown.write(bsd2_markdown)

        # Success if both overridden license formats are present in the
        # fully-qualified result; the stock version of 'bsd2' licenses
        # in the 'system' path should not appear in the listing.
        self.config.licenses_probe()
        overridden_licenses = set(self.config.licenses_list(fullname=True))
        self.assertIn(bsd2_text_name, overridden_licenses)
        self.assertIn(bsd2_markdown_name, overridden_licenses)
        self.assertNotIn(system_license_path + "bsd2.txt", overridden_licenses)
        self.assertNotIn(system_license_path + "bsd2.md", overridden_licenses)
        os.remove(bsd2_text_name)
        os.remove(bsd2_markdown_name)

    def test_licenses_probe(self):
        zlib_text = (
            "This software is provided 'as-is', without any express\n"
            "or implied warranty. In no event will the authors be held\n"
            "liable for any damages arising from the use of this software.\n\n"
            "Permission is granted to anyone to use this software for any\n"
            "purpose, including commercial applications, and to alter it and\n"
            "redistribute it freely, subject to the following "
            "restrictions:\n\n"
            "1. The origin of this software must not be misrepresented;\n"
            "you must not claim that you wrote the original software.\n"
            "If you use this software in a product, an acknowledgement\n"
            "in the product documentation would be appreciated but is not "
            "required.\n"
            "2. Altered source versions must be plainly marked as such,\n"
            "and must not be misrepresented as being the original software.\n"
            "3. This notice may not be removed or altered from any source\n"
            "distribution.\n")
        zlib_markdown = (
            "Licensed under the Zlib License.  \n"
            "Distributed under the Zlib License.  \n\n")
        zlib_text_name = self.tmp_dir.name + "zlib.txt"
        zlib_markdown_name = self.tmp_dir.name + "zlib.md"

        # Sets the 'user' 'license' path to the temporary directory
        # so all the licenses created in this test case would be
        # automatically removed upon completion (by the 'tearDown')
        self.config.paths_set(license=self.tmp_dir.name)

        # License-text only test: fail because the lack of corresponding
        # markdown file
        with open(zlib_text_name, "w") as license_text:
            license_text.write(zlib_text)

        with self.assertRaises(FileNotFoundError):
            self.config.licenses_probe()

        os.remove(zlib_text_name)

        # License-markdown only test: fail because the lack of corresponding
        # text file
        with open(zlib_markdown_name, "w") as license_markdown:
            license_markdown.write(zlib_markdown)

        with self.assertRaises(FileNotFoundError):
            self.config.licenses_probe()

        os.remove(zlib_markdown_name)

        # Success since there is no new custom license
        self.config.licenses_probe()

        # Success due to the existence of both text and markdown format
        # of the given license
        with open(zlib_text_name, "w") as license_text:
            license_text.write(zlib_text)

        with open(zlib_markdown_name, "w") as license_markdown:
            license_markdown.write(zlib_markdown)

        self.config.licenses_probe()
        self.assertIn("zlib", self.config.licenses_list())
        os.remove(zlib_text_name)
        os.remove(zlib_markdown_name)

    def test_licenses_validate(self):
        # Cannot be tested since the 'system' license path is hardcoded
        # and within this test suite assumption like
        # "the full skaff program is installed properly in the system"
        # cannot be made: the test suite may be launched prior to the
        # installation of the "skaff" program, if at all.
        pass

    def test_paths_set(self):
        keys = ("config", "license", "template")
        random_key = "random"
        paths = dict.fromkeys(keys)

        # Fail due to 'None' values
        with self.assertRaises(ValueError):
            self.config.paths_set(**paths)

        # Fail due to invalid key-value argument
        with self.assertRaises(ValueError):
            self.config.paths_set(random_key=random_key)

        # Fail due to invalid value argument
        paths["config"] = self.tmp_dir.name
        paths["license"] = paths["config"] + "license" + os.sep
        paths["template"] = 0
        with self.assertRaises(ValueError):
            self.config.paths_set(**paths)

        paths["template"] = paths["config"] + "template" + os.sep
        self.config.paths_set(**paths)

        self.config.paths_set()
        self.assertTrue(all(self.config.paths_get()))

    def test_paths_get(self):
        keys = ("config", "license", "template")
        result_dict = None
        result_list = None

        # Fail due to 'None' type argument
        with self.assertRaises(TypeError):
            self.config.paths_get(None)

        # Success if the dictionary returned is a deep copy;
        # so the internal 'database' would not be accidentally altered
        self.config.paths_set()
        result_dict = self.config.paths_get()
        for key in keys:
            result_dict[key] = None
            self.assertIsInstance(self.config.paths_get(key), str)

        # Success if the list returned contains the corresponding paths
        # of the keys given
        self.config.paths_set()
        result_list = self.config.paths_get(*keys)
        for result in result_list:
            self.assertIsInstance(result, str)

    def test_quiet_set(self):
        self.config.quiet_set(None)
        self.assertIsInstance(self.config.quiet_get(), bool)

        with self.assertRaises(TypeError):
            self.config.quiet_set(str())

    def test_quiet_get(self):
        options = (True, False)

        for option in options:
            self.config.quiet_set(option)
            self.assertEqual(option, self.config.quiet_get())

    def test_subdirectories_set(self):
        # Identical to 'test_directories_set' because the similarity between
        # the 2 mutator member functions; may be expanded later on if new
        # checking branches are added to 'subdirectories_set'
        subdirectories = ["Opportunity" + os.sep,
                          "Curiosity" + os.sep,
                          lambda x: not x]

        # Fail due to non-iterable type
        with self.assertRaises(TypeError):
            self.config.subdirectories_set(subdirectories[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(TypeError):
            self.config.subdirectories_set(subdirectories[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.subdirectories_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(TypeError):
            self.config.subdirectories_set(subdirectories)

        subdirectories[-1] = "\t"
        # Fail due to the existence of non-printable string
        with self.assertRaises(ValueError):
            self.config.subdirectories_set(subdirectories)

        # Success
        del subdirectories[-1]
        self.config.subdirectories_set(subdirectories)
        self.assertCountEqual(subdirectories, self.config.subdirectories_get())

    def test_subdirectory_add(self):
        # Again, identical to 'test_directory_add'.
        # This "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        subdirectory_added = "Unix"
        counter = None

        # Fail due to wrong type for the 'directory' argument
        with self.assertRaises(TypeError):
            self.config.subdirectory_add(None)

        # Fail because the 'directory' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.subdirectory_add(str())

        # Fail because the 'directory' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.subdirectory_add("\t")

        for _ in range(add_count):
            self.config.subdirectory_add(subdirectory_added)
        # Success if 'directory_add' actually added the specified 'directory'
        self.assertIn(subdirectory_added + os.sep,
                      self.config.subdirectories_get())

        counter = collections.Counter(self.config.subdirectories_get())
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertEqual(1, counter[subdirectory_added + os.sep])

    def test_subdirectory_discard(self):
        # Again, identical to 'test_directory_discard'.
        # This "magic number" is questionable;
        # but to maintain "test reproducibility" it is kept this way
        add_count = 10
        subdirectory_discarded = "Multics"

        # Fail due to wrong type for the 'author' argument
        with self.assertRaises(TypeError):
            self.config.subdirectory_discard(None)

        # Fail because the 'author' argument cannot be an empty string
        with self.assertRaises(ValueError):
            self.config.subdirectory_discard(str())

        # Fail because the 'author' argument cannot contain non-printables
        with self.assertRaises(ValueError):
            self.config.subdirectory_discard("\t")

        # The path separator will be automatically added in both
        # 'directory_add' and 'directory_discard' member functions
        for _ in range(add_count):
            self.config.subdirectory_add(subdirectory_discarded)
        self.config.subdirectory_discard(subdirectory_discarded)
        # Success if the underlying representation
        # for authors does not permit duplicates
        self.assertNotIn(subdirectory_discarded,
                         self.config.subdirectories_get())
        self.assertNotIn(subdirectory_discarded + os.sep,
                         self.config.subdirectories_get())

    def test_subdirectories_get(self):
        # Test directory names with non-ascii characters
        subdirectories = ["Луноход" + os.sep, "玉兔" + os.sep]
        get_result = None

        self.config.subdirectories_set(subdirectories)
        get_result = self.config.subdirectories_get()
        self.assertCountEqual(subdirectories, get_result)
# --------------------------------- CLASSES -----------------------------------

if __name__ == "__main__":
    unittest.main()
