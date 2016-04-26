#!/usr/bin/env python3

from setuptools import find_packages, setup

if __name__ == "__main__":
    genmake_description = "CMake-based project generator"
    genmake_long_description = "Simple script that generates " +\
        "language specific (c/c++) cmake based project structures"

    # This script and MANIFEST.in file are based on the guide at
    # https://pythonhosted.org/setuptools/setuptools.html
    # and
    # https://python-packaging.readthedocs.org/en/latest/index.html
    # Classifier List
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    setup(name="genmake",
          version="0.3",
          description=genmake_description,
          long_description=genmake_long_description,
          # "Development Status :: 2 - Pre-Alpha",
          # "Development Status :: 4 - Beta",
          # "Development Status :: 5 - Production/Stable",
          # "Natural Language :: English",
          classifiers=[
              "Development Status :: 3 - Alpha",
              "Environment :: Console",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: BSD License",
              "Operating System :: POSIX",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.2",
              "Programming Language :: Python :: 3.3",
              "Programming Language :: Python :: 3.4",
              "Programming Language :: Python :: 3.5",
              "Topic :: Software Development :: Build Tools"
          ],
          keywords="cmake",
          url="http://github.com/jhxie/genmake",
          author="Jiahui Xie",
          author_email="jxie2@ualberta.ca",
          license="BSD",
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
          # All the files listed in 'MANIFEST.in' will be installed, too
          include_package_data=True,
          zip_safe=False)
