|skaff|

Overview
--------

| Skaff is a Python library for building programming language dependent
  scaffolding of software projects, and a command-line tool that uses this
  library with built-in (CMake-based) C/C++ support.
| Click any of the following badges to see details.
| |Documentation Status| |License| |Build Status|

Getting Started
---------------

To create a project directory named *nihil*:

.. code:: bash

    skaff nihil

| then a directory tree like the following will be created
  (configuration files are not shown):
| |tree|

Show usage help by:

.. code:: bash

    skaff --help

For the detailed command-line reference manual, use *man* as usual:

.. code:: bash

    man 1 skaff

| A few more examples along with its detailed developers' documentation
  will be
  given on `ReadTheDocs <http://skaff.readthedocs.io/en/latest/>`__
  later on.

Versioning
----------

| Before version **v0.5** this project is in alpha stage, there may be
  serious bugs.
| Beta stage starts at **v0.5** at which point all the necessary test
  cases would be added.
| Once the version number gets to **v1.0** it goes out of beta stage and
  would be released on `PyPI <https://pypi.python.org/pypi>`__ as well; more
  features may be added later on.
| The change log can be viewed `here <CHANGELOG.rst>`__.

Dependency
----------

- Python 3.5+
- Setuptools 20.0+

| Once downloaded, make sure the version of python is **at least 3.5**:

.. code:: bash

    which python3 && python3 --version

| And also remember to have **python3-setuptools** installed:
| **Ubuntu** (>= 16.04)

.. code:: bash

    sudo apt-get install python3-setuptools

| **FreeBSD** (>= 10.3)
| The *pkg* package manager requires a *specific* version number; unlike the
  Ubuntu linux distribution listed above, so either install a version that
  supports python version **3.5** or use the following command to install the
  most recent version:

.. code:: bash

    sudo pkg install `pkg search -ce 'Python packages installer' | sort | awk 'END{print $1}'`

| To ensure there is no problems caused by Python version skew, run the bundled
  unit test suite (done automatically by the continuous integration system):

.. code:: bash

    python3 ./setup.py test


Installation
------------

| As mentioned in the *Versioning* section, for now the only way to get the
  package is here as well as the
  `BitBucket mirror <https://bitbucket.org/jhxie/skaff>`__;
  there is no *binary* (or *compiled-bytecode,* if you prefer) package
  available.

| First grab the source code from here and then simply change directory to
  where the un-compressed source directory resides and install by:

.. code:: bash

    sudo python3 ./setup.py install --optimize 1 --record install_log.txt

| Alternatively, to install (mininal changes to the file system: only a single
  python script pointing to the 'cli.py' executable of source directory is
  actually installed to one of the system **$PATH**; manual pages and
  system-wide configuration files are not installed) the development version:

.. code:: bash

    sudo python3 ./setup.py develop

| To uninstall the *skaff* program along with its data and manual pages
  (before doing so, make sure there is **no whitespace character** in all the
  paths recorded in the *install\_log.txt* file created by the previous
  *install* pass; you have been **warned**):

.. code:: bash

    cat install_log.txt | sudo xargs rm -rf
    sudo mandb

To uninstall the development version:

.. code:: bash

    sudo python3 ./setup.py develop --uninstall
    which skaff && sudo rm `which skaff`

Supported Platforms
-------------------

-  Linux
-  FreeBSD
-  Mac OS X (haven't tested, but I see no reason why it doesn't work)

Credit
------

-  `CMake <https://cmake.org>`__ is developed and maintained by Kitware.
-  The colorscheme of Skaff's logo is inspired by this
   `example <http://i34.photobucket.com/albums/d142/JanetB0601/ColorComboChallenge72.jpg>`__.
-  The **BSD-2-Clause** badge is from
   `here <https://github.com/demhydraz/badge-collection>`__.
-  `Inkscape <https://inkscape.org/>`__ is used to design the original
   SVG format logo.
-  Motivation from Douglas Mcilroy: "*As a programmer, it is your job to put
   yourself out of business. What you do today can be automated tomorrow.*"

License
-------

| Copyright © 2016, Jiahui Xie
| Licensed under the `BSD 2-Clause
  License <https://opensource.org/licenses/BSD-2-Clause>`__.
| Distributed under the `BSD 2-Clause
  License <https://opensource.org/licenses/BSD-2-Clause>`__.

.. |skaff| image:: img/banner.png
.. |Documentation Status| image:: https://readthedocs.org/projects/skaff/badge/?version=latest
   :target: http://skaff.readthedocs.io/en/latest/?badge=latest
.. |License| image:: https://img.shields.io/badge/license-BSD%202--Clause-blue.svg
   :target: http://opensource.org/licenses/BSD-2-Clause
.. |Build Status| image:: https://semaphoreci.com/api/v1/jhxie/skaff/branches/master/badge.svg
   :target: https://semaphoreci.com/jhxie/skaff
.. |tree| image:: doc/source/img/output_tree.png

