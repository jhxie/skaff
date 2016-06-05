#!/usr/bin/env python3

"""
Unit testing suite for core module.
"""
# --------------------------------- MODULES -----------------------------------
import os
import pwd
import unittest

from tempfile import TemporaryDirectory

# Avoid import globbing: each function is imported separately instead.
import skaff
# --------------------------------- MODULES -----------------------------------


class TestCore(unittest.TestCase):
    """
    Main unit testing suite, which is a subclass of 'unittest.TestCase'.
    """
    def test_skaff(self):
        argument_dict = dict(author=None, directories=("project"),
                             language=None, license=None,
                             quiet=True)
        # Fail due to wrong type for 'directories' argument
        with self.assertRaises(ValueError):
            skaff.skaff(**argument_dict)

        argument_dict["directories"] = list()

        # Fail due to empty 'directories' argument
        with self.assertRaises(ValueError):
            skaff.skaff(**argument_dict)

        # Fail due to pre-existing 'project' directory
        argument_dict["directories"] = ["project"]
        os.mkdir(argument_dict["directories"][0])
        with self.assertRaises(FileExistsError):
            skaff.skaff(**argument_dict)
        os.rmdir(argument_dict["directories"][0])

    def test_skaff_version_get(self):
        self.assertTrue(skaff.skaff_version_get())

    def test__author_get(self):
        # Get system password database record based on current user UID
        pw_record = pwd.getpwuid(os.getuid())

        # '_author_get()' must return identical term if GECOS field is defined
        if pw_record.pw_gecos:
            self.assertEqual(skaff._author_get(), pw_record.pw_gecos)
        # Otherwise it must matches the current user's login name
        elif pw_record.pw_name:
            self.assertEqual(skaff._author_get(), pw_record.pw_name)
        # If none of the above works, 'RuntimeError' is raised
        else:
            with self.assertRaises(RuntimeError):
                skaff._author_get()

    def test__basepath_find(self):
        basepath = skaff._basepath_find()

        self.assertTrue(os.path.isdir(basepath))
        self.assertTrue(os.path.isabs(basepath))

    def test__conf_edit(self):
        # Omitted because this is an interactive UI-related function
        # and the author does not know how to test it properly
        pass

    def test__conf_spawn(self):
        argument_dict = dict(directory=None, language=None, quiet=True)
        conf_files = frozenset((".editorconfig", ".gdbinit", ".gitattributes",
                                ".gitignore", ".travis.yml", "CMakeLists.txt"))

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            skaff._conf_spawn(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            skaff._conf_spawn(**argument_dict)
            for conf_file in conf_files:
                self.assertTrue(os.path.isfile(tmp_dir + os.sep + conf_file))
            # Fail because of newly spawned configuration files
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            skaff._conf_spawn(**argument_dict)

        # Fail because of unsupported programming languages
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["language"] = "python"
            skaff._conf_spawn(**argument_dict)

    def test__doc_create(self):
        argument_dict = dict(author=None,
                             directory=None,
                             license=None,
                             quiet=True)
        # Use immutable variant of set instead
        licenses = frozenset(("bsd2", "bsd3", "gpl2", "gpl3", "mit"))

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            skaff._doc_create(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            skaff._doc_create(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + os.sep + "CHANGELOG.md"))
            self.assertTrue(os.path.isfile(tmp_dir + os.sep + "Doxyfile"))
            self.assertTrue(os.path.isfile(tmp_dir + os.sep + "README.md"))
            # Fail because of newly created documentation
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            skaff._doc_create(**argument_dict)

        # Fail because of unsupported license
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["license"] = "null"
            skaff._doc_create(**argument_dict)

        # Success since all the licenses are valid
        # ensure that correct 'README.md' is created
        for license in licenses:
            argument_dict["license"] = license
            # Temporary directory will be destroyed after the block
            with TemporaryDirectory() as tmp_dir:
                argument_dict["directory"] = tmp_dir
                skaff._doc_create(**argument_dict)
                with open(tmp_dir + os.sep + "README.md", "r") as readme_file:
                    self.assertIn(license.upper(), readme_file.read())

    def test__conf_doc_prompt(self):
        # Omitted because this is an interactive UI-related function
        # and the author does not know how to test it properly
        pass

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
        argument_dict = dict(directory=None, quiet=True)

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            skaff._doxyfile_generate(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            skaff._doxyfile_generate(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + os.sep + "Doxyfile"))
            # Fail because of newly created documentation
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            skaff._doxyfile_generate(**argument_dict)

    def test__license_sign(self):
        argument_dict = dict(author=None, directory=None, license=None)

        # Fail because 'directory' cannot be empty
        with self.assertRaises(ValueError):
            skaff._license_sign(**argument_dict)

        with TemporaryDirectory() as tmp_dir:
            argument_dict["directory"] = tmp_dir
            skaff._license_sign(**argument_dict)
            self.assertTrue(os.path.isfile(tmp_dir + os.sep + "LICENSE.txt"))
            # Fail because of newly created documentation
            # the 'directory' is no longer empty
            with self.assertRaises(OSError):
                os.rmdir(tmp_dir)

        # Fail because of non-existing 'directory'
        with self.assertRaises(ValueError):
            skaff._license_sign(**argument_dict)

        # Fail because of unsupported license
        with TemporaryDirectory() as tmp_dir, self.assertRaises(ValueError):
            argument_dict["directory"] = tmp_dir
            argument_dict["license"] = "null"
            skaff._license_sign(**argument_dict)

if __name__ == "__main__":
    unittest.main()
