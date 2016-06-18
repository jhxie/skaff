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
        with self.assertRaises(ValueError):
            self.config.authors_set(authors[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(ValueError):
            self.config.authors_set(authors[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.authors_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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

    def test_directories_set(self):
        # Identical to 'test_authors_set' because the similarity between
        # the 2 mutator member functions; may be expanded later on if new
        # checking branches are added to 'directories_set'
        directories = ["Apollo" + os.sep, "Spirit" + os.sep, lambda x: not x]

        # Fail due to non-iterable type
        with self.assertRaises(ValueError):
            self.config.directories_set(directories[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(ValueError):
            self.config.directories_set(directories[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.directories_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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
        # Every license specified in the listing should work.
        for license in self.config.licenses_list():
            self.config.license_set(license)
            self.assertEqual(license, self.config.license_get())

    def test_quiet_set(self):
        self.config.quiet_set(None)
        self.assertIsInstance(self.config.quiet_get(), bool)

        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
            self.config.subdirectories_set(subdirectories[-1])

        # Fail due to non-containerized string type
        with self.assertRaises(ValueError):
            self.config.subdirectories_set(subdirectories[0])

        # Fail due to empty string
        with self.assertRaises(ValueError):
            self.config.subdirectories_set((str(),))

        # Fail due to the existence of non-string type
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
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

if __name__ == "__main__":
    unittest.main()
