#!/usr/bin/env python3

from setuptools import setup

if __name__ == "__main__":
    genmake_description = "Cmake project generator"
    genmake_long_description = "Simple script that generates " +\
        "language specific (c/c++) cmake based project structures"

    # Based on the guide at
    # https://python-packaging.readthedocs.org/en/latest/index.html
    # Classifier List
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    setup(name="genmake",
          version="0.1",
          description=genmake_description,
          long_description=genmake_long_description,
          # "Development Status :: 4 - Beta",
          # "Development Status :: 5 - Production/Stable",
          # "Natural Language :: English",
          classifiers=[
              "Development Status :: 2 - Pre-Alpha",
              "Environment :: Console",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: BSD License",
              "Operating System :: POSIX",
              "Programming Language :: Python :: 3.2",
              "Topic :: Software Development :: Build Tools"
          ],
          url="http://github.com/jhxie/genmake",
          author="Jiahui Xie",
          author_email="jxie2@ualberta.ca",
          license="BSD",
          packages=["genmake"],
          entry_points={
              "console_scripts": ["genmake=genmake.cli:main"]
          },
          # All the files listed in 'MANIFEST.in' will be installed, too
          include_package_data=True,
          zip_safe=False)
