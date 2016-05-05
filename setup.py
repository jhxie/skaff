#!/usr/bin/env python3

# --------------------------------- MODULES -----------------------------------
import gzip
import os
import shutil
import sys

from genmake import __author__, __email__, __license__, __version__
from setuptools import setup
# --------------------------------- MODULES -----------------------------------

if __name__ == "__main__":
    genmake_description = "CMake-based project generator"
    genmake_long_description = "Simple script that generates " +\
        "language specific (c/c++) cmake based project structures"
    install_prefix = os.path.dirname(os.path.abspath(__file__))
    genmake_man_source = install_prefix + "/man/genmake.1"
    genmake_man_target = None

    # This script and MANIFEST.in file are based on the guide at
    # https://pythonhosted.org/setuptools/setuptools.html
    # and
    # https://python-packaging.readthedocs.org/en/latest/index.html
    # Classifier List
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    setup(name="genmake",
          version=__version__,
          description=genmake_description,
          long_description=genmake_long_description,
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
          url="http://github.com/jhxie/genmake",
          author=__author__,
          author_email=__email__,
          license=__license__,
          packages=["genmake"],
          package_data={
              "genmake": [
                  "genmake/config/*.txt",
                  "genmake/config/Doxyfile",
                  "genmake/config/c/*.txt",
                  "genmake/config/cxx/*.txt",
                  "genmake/license/*.md",
                  "genmake/license/*.txt"]
          },
          entry_points={
              "console_scripts": ["genmake=genmake.cli:main"]
          },
          test_suite="genmake.tests",
          # All the files listed in 'MANIFEST.in' will be installed, too
          include_package_data=True,
          zip_safe=False)

    # Note the following would never be executed if permission is not satisfied
    if "install" in sys.argv:
        with os.popen("manpath") as proc:
            genmake_man_target = proc.read().split(":")[0]

        if not genmake_man_target:
            sys.exit("Output of the 'manpath' program cannot be parsed")

        genmake_man_target = genmake_man_target.rstrip()

        for tail in ("/man1/", os.path.basename(genmake_man_source), ".gz"):
            genmake_man_target += tail

        # Based on example from
        # https://docs.python.org/3/library/gzip.html
        with open(genmake_man_source, "rb") as input_manpage:
            with gzip.open(genmake_man_target, "wb") as output_manpage:
                shutil.copyfileobj(input_manpage, output_manpage)

        # Finally rebuild the manpage database
        os.system("mandb")
