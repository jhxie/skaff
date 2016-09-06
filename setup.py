#!/usr/bin/env python3

# --------------------------------- MODULES -----------------------------------
import os
import skaff
import sys

from setuptools import setup
from skaff.info import skaff_description_get
from skaff.manualtools import (
    manuals_install,
    manuals_probe,
    manpath_select
)
# --------------------------------- MODULES -----------------------------------


# -------------------------------- FUNCTIONS ----------------------------------
def main() -> None:
    """
    Main installation subroutine.
    """
    skaff_description = skaff_description_get(short=True)
    skaff_long_description = skaff_description_get(short=False)
    flags = ("--dry-run", "-n", "--help")
    skaff_man_source_dir = (os.path.dirname(os.path.abspath(__file__)) +
                            os.sep + "man" + os.sep)
    skaff_man_sources = manuals_probe(skaff_man_source_dir)
    manual_conditions = (flag not in sys.argv for flag in flags)

    # This whole installation subroutine and 'MANIFEST.in' file are based
    # on the guide at
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
              # module 'typing' is supported starting at 3.5
              "Programming Language :: Python :: 3.5",
              "Topic :: Software Development :: Build Tools"
          ],
          keywords="cmake",
          url="http://github.com/jhxie/skaff",
          author=skaff.__author__,
          author_email=skaff.__email__,
          maintainer=skaff.__maintainer__,
          maintainer_email=skaff.__email__,
          license=skaff.__license__,
          packages=["skaff"],
          package_data={
              "skaff": [
                  "skaff/config/template/*.txt",
                  "skaff/config/template/Doxyfile",
                  "skaff/config/template/travis.yml",
                  "skaff/config/template/c/*.txt",
                  "skaff/config/template/c/src/*",
                  "skaff/config/template/c/include/*",
                  "skaff/config/template/cpp/*.txt",
                  "skaff/config/template/cpp/src/*",
                  "skaff/config/template/cpp/include/*",
                  "skaff/config/license/*.md",
                  "skaff/config/license/*.txt"]
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
    if "install" in sys.argv and all(manual_conditions):
        manuals_install(manpath_select(), True, *skaff_man_sources)
# -------------------------------- FUNCTIONS ----------------------------------


if __name__ == "__main__":
    main()
