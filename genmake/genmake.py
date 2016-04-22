#!/usr/bin/env python3

# --------------------------------- MODULES -----------------------------------
import os
import shutil
# --------------------------------- MODULES -----------------------------------


def genmake(author, directories, language, license):
    """
    """
    print(author)
    _directory_create(directories)
    print(language)
    print(license)


def _directory_create(directories):
    """
    Create all the necessary subdirectories in addition to the project root.
    """
    subdirectories = (
        "build",
        "coccinelle",
        "src",
        "doc",
        "img",
        "tests"
    )

    for base_dir in directories:
        if "/" != base_dir[-1]:
            base_dir += "/"
        os.mkdir(base_dir)

        for sub_dir in subdirectories:
            os.mkdir(base_dir + sub_dir)

        # Create parent directory if it does not exist
        os.makedirs(base_dir + "include/" + os.path.basename(base_dir[:-1]))


def _license_sign(author, license):
    """
    """
    # shutil.copy()


def _conf_spawn(language):
    """
    """
    pass
