![genmake](img/banner.png)

## NOTICE
Development halts temporarily until **2016-06-18**.

## Overview
A CMake-based project scaffolding tool.  
Click any of the following to see details.  
[![Documentation Status](
https://readthedocs.org/projects/genmake/badge/?version=latest)](
http://genmake.readthedocs.io/en/latest/?badge=latest)
[![License](
https://img.shields.io/badge/license-BSD%202--Clause-blue.svg)](
http://opensource.org/licenses/BSD-2-Clause)
[![Build Status](
https://semaphoreci.com/api/v1/jhxie/genmake/branches/master/badge.svg)](
https://semaphoreci.com/jhxie/genmake)

## Versioning
Before version **v0.5** this project is in alpha stage, there may be hidden
bugs.

Beta stage starts at **v0.5** at which point all the necessary test cases would
be added.

Once the version number gets to **v1.0** it goes out of beta stage and would
be released on [PyPI](https://pypi.python.org/pypi) as well; more features may
be added later on.

The changelog can be viewed [here](CHANGELOG.md).

## Installation
As mentioned in the above section, for now the only way to get the package is
here as well as the [BitBucket mirror](https://bitbucket.org/jhxie/genmake);
there is no *binary* (or *compiled-bytecode,* if you prefer) package available.

Once downloaded, make sure you have **python3-setuptools** installed:

**Ubuntu** (14.04 and later)
```bash
sudo apt-get install python3-setuptools
```

**Fedora** (23 and later)
```bash
sudo dnf install python3-setuptools
```
then simply change directory to where the un-compressed source directory
resides and install by:
```bash
python3 ./setup.py clean build
sudo python3 ./setup.py install
```

## Usage
Show usage help by:
```bash
genmake --help
```
For the detailed command-line reference manual, use *man* as usual:
```bash
man 1 genmake
```
A few more examples along with its detailed documentation will be given on
[ReadTheDocs](https://readthedocs.org/projects/genmake/badge/?version=latest)
later on.

## Supported Platforms
* Linux
* FreeBSD
* Mac OS X (haven't tested, but I see no reason why it doesn't work)

## Credit
* [CMake](https://cmake.org) is developed and maintained by Kitware.
* The colorscheme of GenMake's logo is inspired by this
[example
](http://i34.photobucket.com/albums/d142/JanetB0601/ColorComboChallenge72.jpg).
* The **BSD-2-Clause** badge is from [here
](https://github.com/demhydraz/badge-collection).
* [Inkscape](https://inkscape.org/) is used to design the original SVG format
logo.
* Motivation from Douglas Mcilroy: "*As a programmer, it is your job to put
yourself out of business. What you do today can be automated tomorrow.*"

## License
Copyright &copy; 2016 Jiahui Xie  
Licensed under the [BSD 2-Clause License][BSD2].  
Distributed under the [BSD 2-Clause License][BSD2].

[BSD2]: https://opensource.org/licenses/BSD-2-Clause
