#!/usr/bin/env python3

"""
Unit testing suite for info module.
"""
# --------------------------------- MODULES -----------------------------------
import unittest

from skaff.info import (
    skaff_description_get,
    skaff_info_get
)
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class TestInfo(unittest.TestCase):
    """
    Main unit testing suite, which is a subclass of 'unittest.TestCase'.
    """
    def test_skaff_description_get(self):
        # Both short and long descriptions should be non-empty strings.
        self.assertTrue(skaff_description_get(short=True))
        self.assertTrue(skaff_description_get(short=False))

        # The short description needs to be shorter than the long variant.
        short_description_length = skaff_description_get(short=True)
        long_description_length = skaff_description_get(short=False)
        self.assertLessEqual(short_description_length, long_description_length)

    def test_skaff_info_get(self):
        self.assertTrue(skaff_info_get())
# --------------------------------- CLASSES -----------------------------------

if __name__ == "__main__":
    unittest.main()
