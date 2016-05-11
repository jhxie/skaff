![genmake](img/banner.png)

## Overview
An automatic CMake-based project generator.

## Build Status
* [![Build Status](https://travis-ci.org/jhxie/genmake.svg?branch=master)]
(https://travis-ci.org/jhxie/genmake)

## Versioning
Before version **v0.5** this project is in alpha stage, there may be hidden
bugs.

Beta stage starts at **v0.5** at which point all the necessary test cases would
be added.

Once the version number gets to **v1.0** it goes out of beta stage and would
be released on [PyPI](https://pypi.python.org/pypi) as well; more features may
be added later on.

## Installation
As mentioned in the above section, for now the only way to get the package is
here as well as the [BitBucket mirror](https://bitbucket.org/jhxie/genmake);
there is no *binary* package available.

Once downloaded, make sure you have **python3-setuptools** installed:

**Ubuntu**
```bash
sudo apt-get install python3-setuptools
```

**Fedora**
```bash
sudo dnf install python3-setuptools
```
then simply change directory to where the un-compressed source directory
resides and install by:
```bash
python3 ./setup.py clean build
sudo python3 ./setup.py install
```
show usage help by:
```bash
genmake --help
```

## Supported Platforms
* Linux
* FreeBSD
* Mac OS X (haven't tested, but I see no reason why it doesn't work)

## Credit
* The colorscheme of GenMake's logo is inspired by this
[example
](http://i34.photobucket.com/albums/d142/JanetB0601/ColorComboChallenge72.jpg).
* [Inkscape](https://inkscape.org/) is used to design the original SVG format
logo.
* Motivation from Douglas Mcilroy: "*As a programmer, it is your job to put
yourself out of business. What you do today can be automated tomorrow.*"

## License
Copyright &copy; 2016 Jiahui Xie

Licensed under the [BSD 2-Clause License][BSD2].

Distributed under the [BSD 2-Clause License][BSD2].

[BSD2]: https://opensource.org/licenses/BSD-2-Clause
