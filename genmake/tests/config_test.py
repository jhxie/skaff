#!/usr/bin/env python3

"""
Unit testing suite for config module.
"""
# --------------------------------- MODULES -----------------------------------
import unittest

from tempfile import TemporaryDirectory

# Avoid import globbing: each function is imported separately instead.
import genmake
# --------------------------------- MODULES -----------------------------------


class TestConfig(unittest.TestCase):
    """
    Unit testing suite for 'config' module.
    """
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        # NOTE: the 'directories' argument needs to be an iterable;
        # a tuple (denoted by an extra comma inside the parentheses) is used.
        self.config = genmake.GenMakeConfig((self.tmp_dir.name,))

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_authors_set(self):
        pass

    def test_author_add(self):
        pass

    def test_author_discard(self):
        pass

    def test_authors_get(self):
        pass

    def test_author_fetch(self):
        pass

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
