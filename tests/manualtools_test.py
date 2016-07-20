#!/usr/bin/env python3

"""
Unit testing suite for manualtools module.
"""
# --------------------------------- MODULES -----------------------------------
import os
import string
import tempfile
import unittest

from skaff.manualtools import (
    manual_check,
    manuals_install,
    manuals_probe,
)
# --------------------------------- MODULES -----------------------------------


# --------------------------------- CLASSES -----------------------------------
class TestManualTools(unittest.TestCase):
    """
    Unit testing suite for 'manualtools' module.
    """
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        if not self.tmp_dir.name.endswith(os.sep):
            self.tmp_dir.name += os.sep

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_manual_check(self):
        directory = self.tmp_dir.name
        manuals = [directory + "test." + str(digit) for digit in range(1, 10)]

        # Fail due to incompatible type of argument
        with self.assertRaises(TypeError):
            manual_check(None)

        # False due to empty string
        self.assertFalse(manual_check(str()))

        # False due to the second (actual) file extension
        # is not a number in range(1, 10)
        self.assertFalse(manual_check("test.1.xz"))

        # False due to the file extension is not a number in range(1, 10)
        self.assertFalse(manual_check("test.0"))
        self.assertFalse(manual_check("test.11"))

        # Success regardless the manuals are prefixed by any directories
        self.assertTrue(all(manual_check(manual) for manual in manuals))

        manuals = [os.path.basename(manual) for manual in manuals]
        self.assertTrue(all(manual_check(manual) for manual in manuals))

    def test_manuals_install(self):
        isfile = os.path.isfile
        basename = os.path.basename
        directory = self.tmp_dir.name
        custom_man_path = directory + "man" + os.sep
        manuals = [directory + "test." + str(digit) for digit in range(1, 10)]

        # Fail due to non-existing target directory
        with self.assertRaises(NotADirectoryError):
            manuals_install(custom_man_path, False, *manuals)

        os.mkdir(custom_man_path)

        # Fail due to non-existing manuals
        with self.assertRaises(FileNotFoundError):
            manuals_install(custom_man_path, False, *manuals)

        for manual in manuals:
            with open(manual, "w"):
                pass

        manuals_install(custom_man_path, False, *manuals)

        # Success - manuals are installed to the base directory
        for manual in manuals:
            self.assertTrue(isfile(custom_man_path + basename(manual) + ".gz"))

        # Success - manuals are installed to the subdirectory that ends with
        # an extra manual page section number
        for digit, manual in zip(range(1, 10), manuals):
            manpath_subdir = custom_man_path + "man" + str(digit) + os.sep
            os.mkdir(manpath_subdir)
            manuals_install(manpath_subdir, False, manual)
            self.assertTrue(isfile(manpath_subdir + basename(manual) + ".gz"))

    def test_manuals_probe(self):
        directory = self.tmp_dir.name
        dummy_file = None
        dummy_dir = None
        file_entries = {directory + "test." + digit for digit in string.digits}
        file_entries.add(directory + "test")

        # Fail due to the argument given is a file, not directory
        with tempfile.NamedTemporaryFile() as tmp_file:
            dummy_file = tmp_file.name
            with self.assertRaises(NotADirectoryError):
                manuals_probe(dummy_file)

        # Fail due to non-existing file
        with self.assertRaises(NotADirectoryError):
            manuals_probe(dummy_file)

        # Fail due to non-existing directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_dir = tmp_dir

        with self.assertRaises(NotADirectoryError):
            manuals_probe(dummy_dir)

        # Success if the list result is empty:
        # which should be the case since the 'directory' is empty
        self.assertEqual(len(manuals_probe(directory)), 0)

        # Creates dummy files in 'file_entries' with two files considered
        # "un-qualified" as manual pages in unix man-page format:
        # 'test' 'test.0'
        for file_entry in file_entries:
            with open(file_entry, "w"):
                pass

        result_manuals = manuals_probe(directory)
        file_entries.discard(directory + "test")
        file_entries.discard(directory + "test.0")
        self.assertSequenceEqual(result_manuals, sorted(file_entries))

        # From the official documentation hosted at:
        # https://docs.python.org/3.5/library/tempfile.html
        # "
        # On completion of the context or destruction of the temporary
        # directory object the newly created temporary directory and all its
        # contents are removed from the filesystem.
        # "
        # so there is no need to call something like 'os.remove' for files in
        # the original 'file_entries' set.

    def test_manpath_select(self):
        # Untested because the author does not know how to inject a mock
        # 'manpath' program into the 'manpath_select' function without adding
        # an extra formal parameter for it.
        pass
# --------------------------------- CLASSES -----------------------------------

if __name__ == "__main__":
    unittest.main()
