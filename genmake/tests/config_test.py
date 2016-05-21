#!/usr/bin/env python3

"""
Unit testing suite for config module.
"""
# --------------------------------- MODULES -----------------------------------
import unittest

# Avoid import globbing: each function is imported separately instead.
import genmake
# --------------------------------- MODULES -----------------------------------


class TestConfig(unittest.TestCase):
    """
    Main unit testing suite, which is a subclass of 'unittest.TestCase'.
    """
    def test_authors_set(self):
        pass

    def test_author_get(self):
        pass

    def test_author_fetch(self):
        pass

    def test_directories_set(self):
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
