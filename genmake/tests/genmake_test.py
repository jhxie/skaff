#!/usr/bin/env python3

"""
Unit testing suite for genmake module.
"""
# --------------------------------- MODULES -----------------------------------
import unittest

# Avoid import globbing: each function is imported separately instead.
from genmake.genmake import genmake
from genmake.genmake import _author_get
from genmake.genmake import _basepath_find
from genmake.genmake import _conf_spawn
from genmake.genmake import _doc_create
from genmake.genmake import _license_sign
# --------------------------------- MODULES -----------------------------------


class TestGenMake(unittest.TestCase):
    """
    """
    def test_genmake(self):
        argument_dict = dict(author=None, directories=("project"),
                             language=None, license=None,
                             quiet=True)
        # Fail due to wrong type for 'directories' argument
        with self.assertRaises(ValueError):
            genmake(**argument_dict)

        argument_dict["directories"] = list()

        # Fail due to empty 'directories' argument
        with self.assertRaises(ValueError):
            genmake(**argument_dict)

        argument_dict["directories"] = ["project"]

    def test__author_get(self):
        pass

    def test__basepath_find(self):
        pass

    def test__conf_spawn(self):
        pass

    def test__doc_create(self):
        pass

    def test__license_sign(self):
        pass


if __name__ == "__main__":
    unittest.main()
