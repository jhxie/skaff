#!/usr/bin/env python3

"""
Unit testing suite for genmake module.
"""
# --------------------------------- MODULES -----------------------------------
import os
import pwd
import unittest

from tempfile import TemporaryDirectory

# Avoid import globbing: each function is imported separately instead.
from genmake import genmake
from genmake import genmake_version_get
from genmake import _author_get
from genmake import _basepath_find
from genmake import _conf_spawn
from genmake import _doc_create
from genmake import _doc_create_prompt
from genmake import _license_sign
# --------------------------------- MODULES -----------------------------------


class TestGenMake(unittest.TestCase):
    """
    Main unit testing suite, which is a subclass of 'unittest.TestCase'.
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

        # Fail due to pre-existing 'project' directory
        argument_dict["directories"] = ["project"]
        os.mkdir(argument_dict["directories"][0])
        with self.assertRaises(FileExistsError):
            genmake(**argument_dict)
        os.rmdir(argument_dict["directories"][0])

    def test_genmake_version_get(self):
        self.assertTrue(genmake_version_get())

    def test__author_get(self):
        # Get system password database record based on current user UID
        pw_record = pwd.getpwuid(os.getuid())

        # '_author_get()' must return identical term if GECOS field is defined
        if pw_record.pw_gecos:
            self.assertEqual(_author_get(), pw_record.pw_gecos)
        # Otherwise it must matches the current user's login name
        elif pw_record.pw_name:
            self.assertEqual(_author_get(), pw_record.pw_name)
        # If none of the above works, 'RuntimeError' is raised
        else:
            with self.assertRaises(RuntimeError):
                _author_get()

    def test__basepath_find(self):
        basepath = _basepath_find()

        self.assertTrue(os.path.isdir(basepath))
        self.assertTrue(os.path.isabs(basepath))

    def test__conf_spawn(self):
        argument_dict = dict(directory=None, language=None, quiet=True)

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            _conf_spawn(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            _conf_spawn(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + "/CMakeLists.txt"))
            # Fail because of newly spawned configuration files
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            _conf_spawn(**argument_dict)

        # Fail because of unsupported programming languages
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["language"] = "python"
            _conf_spawn(**argument_dict)

    def test__doc_create(self):
        argument_dict = dict(author=None,
                             directory=None,
                             license=None,
                             quiet=True)
        # Use immutable variant of set instead
        licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            _doc_create(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            _doc_create(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + "/Doxyfile"))
            self.assertTrue(os.path.isfile(tmp_dir + "/README.md"))
            # Fail because of newly created documentation
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            _doc_create(**argument_dict)

        # Fail because of unsupported license
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["license"] = "null"
            _doc_create(**argument_dict)

        # Success since all the licenses are valid
        # ensure that correct 'README.md' is created
        for license in licenses:
            argument_dict["license"] = license
            # Temporary directory will be destroyed after the block
            with TemporaryDirectory() as tmp_dir:
                argument_dict["directory"] = tmp_dir
                _doc_create(**argument_dict)
                with open(tmp_dir + "/README.md", "r") as readme_file:
                    self.assertIn(license.upper(), readme_file.read())

    def test__license_sign(self):
        argument_dict = dict(author=None, directory=None, license=None)

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            _license_sign(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            _license_sign(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + "/LICENSE.txt"))
            # Fail because of newly created documentation
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            _license_sign(**argument_dict)

        # Fail because of unsupported license
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["license"] = "null"
            _license_sign(**argument_dict)

if __name__ == "__main__":
    unittest.main()
