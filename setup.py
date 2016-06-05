#!/usr/bin/env python3

# --------------------------------- MODULES -----------------------------------
import skaff
import gzip
import os
import shutil
import sys

from filecmp import dircmp
from setuptools import setup
from tempfile import TemporaryDirectory
# --------------------------------- MODULES -----------------------------------


def main():
    """
    Main installation routine.
    """
    skaff_description = "A CMake-Based Project Scaffolding Tool"
    skaff_long_description = "Simple program that generates " +\
        "language specific (c/c++) cmake based project templates"

    # This script and MANIFEST.in file are based on the guide at
    # https://pythonhosted.org/setuptools/setuptools.html
    # and
    # https://python-packaging.readthedocs.org/en/latest/index.html
    # Classifier List
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    setup(name="skaff",
          version=skaff.__version__,
          description=skaff_description,
          long_description=skaff_long_description,
          # "Development Status :: 2 - Pre-Alpha",
          # "Development Status :: 3 - Alpha",
          # "Development Status :: 5 - Production/Stable",
          # "Natural Language :: English",
          classifiers=[
              "Development Status :: 4 - Beta",
              "Environment :: Console",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: BSD License",
              "Operating System :: POSIX",
              "Programming Language :: Python :: 3",
              # 'shutil.get_terminal_size()' is supported starting at 3.3
              "Programming Language :: Python :: 3.3",
              "Programming Language :: Python :: 3.4",
              "Programming Language :: Python :: 3.5",
              "Topic :: Software Development :: Build Tools"
          ],
          keywords="cmake",
          url="http://github.com/jhxie/skaff",
          author=skaff.__author__,
          author_email=skaff.__email__,
          license=skaff.__license__,
          packages=["skaff"],
          package_data={
              "skaff": [
                  "skaff/config/*.txt",
                  "skaff/config/Doxyfile",
                  "skaff/config/travis.yml",
                  "skaff/config/c/*.txt",
                  "skaff/config/c/src/*",
                  "skaff/config/cpp/*.txt",
                  "skaff/config/cpp/src/*",
                  "skaff/license/*.md",
                  "skaff/license/*.txt"]
          },
          entry_points={
              "console_scripts": ["skaff=skaff.cli:main"]
          },
          test_suite="tests",
          # All the files listed in 'MANIFEST.in' will be installed, too
          include_package_data=True,
          zip_safe=False)

    # Note the following would not be properly executed
    # if permission is not satisfied
    if "install" in sys.argv:
        manual_install()


def manual_install():
    """
    Installs the gzipped manual page to one of the non-empty 'manpath'.
    """
    install_prefix = os.path.dirname(os.path.abspath(__file__))
    skaff_man_source = install_prefix + "/man/skaff.1"
    skaff_man_candidates = None
    skaff_man_target = None

    with os.popen("manpath") as proc, TemporaryDirectory() as tmpdir:
        skaff_man_candidates = proc.read().strip().split(os.pathsep)
        for candidate in skaff_man_candidates:
            # "Elect" the candidate directory with "rich" non-empty status
            if dircmp(candidate, tmpdir).left_only:
                skaff_man_target = candidate
                break

    if not skaff_man_candidates:
        sys.exit("Output of the 'manpath' program cannot be parsed")

    if not skaff_man_target:
        sys.exit("All the directories specified in 'manpath' is empty")

    # 'skaff' program belongs to "Section 1: User Commands and Tools"
    for tail in ("/man1/", os.path.basename(skaff_man_source), ".gz"):
        skaff_man_target += tail

    # Based on example from
    # https://docs.python.org/3/library/gzip.html
    with open(skaff_man_source, "rb") as input_manpage:
        with gzip.open(skaff_man_target, "wb") as output_manpage:
            shutil.copyfileobj(input_manpage, output_manpage)

    # Finally rebuild the manpage database
    os.system("mandb")


if __name__ == "__main__":
    main()
