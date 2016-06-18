#!/usr/bin/env python3

"""
Unit testing suite for core module.
"""
# --------------------------------- MODULES -----------------------------------
import os
import unittest

from tempfile import TemporaryDirectory

# Avoid import globbing: each function is imported separately instead.
import skaff
# --------------------------------- MODULES -----------------------------------


class TestCore(unittest.TestCase):
    """
    Main unit testing suite, which is a subclass of 'unittest.TestCase'.
    """
    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        if not self.tmp_dir.name.endswith(os.sep):
            self.tmp_dir.name += os.sep
        # NOTE: the 'directories' argument needs to be an iterable;
        # a tuple (denoted by an extra comma inside the parentheses) is used.
        self.config = skaff.SkaffConfig((self.tmp_dir.name,))

    def tearDown(self):
        # No need to invoke 'directory_discard' since for each test member
        # function a new 'SkaffConfig' instance is created.
        self.tmp_dir.cleanup()

    def test_skaff(self):
        # Fail due to wrong type for the 'config' argument
        with self.assertRaises(ValueError):
            skaff.skaff(None)

        # Fail due to pre-existing directory
        with self.assertRaises(FileExistsError):
            skaff.skaff(self.config)

    def test_skaff_version_get(self):
        self.assertTrue(skaff.skaff_version_get())

    def test__arguments_check(self):
        # Fail because 'directory' does not exist
        with self.assertRaises(ValueError):
            # This 'tmp_dir' only exist within the scope of context manager
            with TemporaryDirectory() as tmp_dir:
                self.config.directory_add(tmp_dir)
            skaff._arguments_check(tmp_dir, self.config)
        self.config.directory_discard(tmp_dir)

        # Fail because 'directory' is not in 'config'
        with self.assertRaises(ValueError):
            self.config.directory_discard(self.tmp_dir.name)
            skaff._arguments_check(self.tmp_dir.name, self.config)
        self.config.directory_add(self.tmp_dir.name)

    def test__basepath_find(self):
        basepath = skaff._basepath_find()

        self.assertTrue(os.path.isdir(basepath))
        self.assertTrue(os.path.isabs(basepath))

    def test__conf_doc_prompt(self):
        # Omitted because this is an interactive UI-related function
        # and the author does not know how to test it properly
        pass

    def test__conf_edit(self):
        # Omitted because this is an interactive UI-related function
        # and the author does not know how to test it properly
        pass

    def test__conf_spawn(self):
        conf_files = frozenset((".editorconfig", ".gdbinit", ".gitattributes",
                                ".gitignore", ".travis.yml", "CMakeLists.txt"))

        skaff._conf_spawn(self.tmp_dir.name, self.config)
        for conf_file in conf_files:
            self.assertTrue(os.path.isfile(self.tmp_dir.name + conf_file))
        # Fail because of newly spawned configuration files
        # the 'directory' is no longer empty
        with self.assertRaises(OSError):
            os.rmdir(self.tmp_dir.name)

    def test__doc_create(self):
        # Use immutable variant of set instead
        docs = frozenset(("CHANGELOG.md", "Doxyfile", "README.md"))
        licenses = frozenset(self.config.licenses_list())

        skaff._doc_create(self.tmp_dir.name, self.config)
        for doc in docs:
            self.assertTrue(os.path.isfile(self.tmp_dir.name + doc))
        # Fail because of newly created documentation
        # the 'directory' is no longer empty
        with self.assertRaises(OSError):
            os.rmdir(self.tmp_dir.name)

        # Success since all the licenses are valid
        # ensure that correct 'README.md' is created
        for license in licenses:
            self.config.license_set(license)
            skaff._doc_create(self.tmp_dir.name, self.config)
            with open(self.tmp_dir.name + "README.md", "r") as readme_file:
                self.assertIn(license.upper(), readme_file.read())

    def test__doxyfile_attr_match(self):
        argument_dict = dict(project_name="Project", line=None)
        attr_dict = {"PROJECT_NAME":
                     "\"{project_name}\"".format(**argument_dict),
                     "OUTPUT_DIRECTORY": "./doc",
                     "TAB_SIZE": 8,
                     "EXTRACT_ALL": "YES",
                     "EXTRACT_STATIC": "YES",
                     "RECURSIVE": "YES",
                     "EXCLUDE": "build",
                     "HAVE_DOT": "YES",
                     "UML_LOOK": "YES",
                     "TEMPLATE_RELATIONS": "YES",
                     "CALL_GRAPH": "YES",
                     "DOT_IMAGE_FORMAT": "svg",
                     "INTERACTIVE_SVG": "YES"}

        # Fail because both arguments have to be non-empty strings
        with self.assertRaises(ValueError):
            skaff._doxyfile_attr_match(project_name=None, line=None)

        with self.assertRaises(ValueError):
            skaff._doxyfile_attr_match(project_name="Project", line=None)

        with self.assertRaises(ValueError):
            skaff._doxyfile_attr_match(project_name=None, line="PlaceHolder")

        # Fail because the project name cannot be solely composed of
        # a single separator character
        with self.assertRaises(ValueError):
            skaff._doxyfile_attr_match(project_name=os.sep, line="PlaceHolder")

        for attr in attr_dict:
            argument_dict["line"] = attr + " = "
            self.assertEqual(skaff._doxyfile_attr_match(**argument_dict),
                             argument_dict["line"] + str(attr_dict[attr]) +
                             "\n")

    def test__doxyfile_generate(self):
        skaff._doxyfile_generate(self.tmp_dir.name, self.config)
        self.assertTrue(os.path.isfile(self.tmp_dir.name + "Doxyfile"))
        # Fail because of newly created documentation
        # the 'directory' is no longer empty
        with self.assertRaises(OSError):
            os.rmdir(self.tmp_dir.name)

    def test__license_sign(self):
        skaff._license_sign(self.tmp_dir.name, self.config)
        self.assertTrue(os.path.isfile(self.tmp_dir.name + "LICENSE.txt"))
        # Fail because of newly created documentation
        # the 'directory' is no longer empty
        with self.assertRaises(OSError):
            os.rmdir(self.tmp_dir.name)

if __name__ == "__main__":
    unittest.main()
