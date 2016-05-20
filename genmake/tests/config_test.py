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
    pass

if __name__ == "__main__":
    unittest.main()
