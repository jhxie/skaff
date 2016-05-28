#!/usr/bin/env python3

"""
Unit testing suite for config module.
"""
# --------------------------------- MODULES -----------------------------------
import collections
import os
import pwd
import unittest

from genmake import GenMakeConfig
from tempfile import TemporaryDirectory
# --------------------------------- MODULES -----------------------------------


class TestConfig(unittest.TestCase):
    """
    Unit testing suite for 'config' module.
    """
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        # NOTE: the 'directories' argument needs to be an iterable;
        # a tuple (denoted by an extra comma inside the parentheses) is used.
        self.config = GenMakeConfig((self.tmp_dir.name,))

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_authors_set(self):
        pass

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
        pass

    def test_author_fetch(self):
        # Get system password database record based on current user UID
        pw_record = pwd.getpwuid(os.getuid())

        # '_author_get()' must return identical term if GECOS field is defined
        if pw_record.pw_gecos:
            self.assertEqual(GenMakeConfig.author_fetch(), pw_record.pw_gecos)
        # Otherwise it must matches the current user's login name
        elif pw_record.pw_name:
            self.assertEqual(GenMakeConfig.author_fetch(), pw_record.pw_name)
        # If none of the above works, 'RuntimeError' is raised
        else:
            with self.assertRaises(RuntimeError):
                GenMakeConfig.author_fetch()

    def test_directories_set(self):
        pass

    def test_directory_add(self):
        pass

    def test_directory_discard(self):
        pass

    def test_directories_get(self):
        pass

    def test_language_set(self):
        pass

    def test_language_get(self):
        pass

    def test_license_set(self):
        pass

    def test_license_get(self):
        pass

    def test_quiet_set(self):
        pass

    def test_quiet_get(self):
        pass

if __name__ == "__main__":
    unittest.main()
