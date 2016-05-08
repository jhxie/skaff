#!/usr/bin/env python3

__all__ = ["clitools", "core"]

# To keep older scripts who import this from breaking -- DEPRECATED
from genmake.clitools import single_keypress_read
from genmake.clitools import timeout
from genmake.clitools import ANSIColor
from genmake.clitools import TimeOutError
from genmake.core import genmake
from genmake.core import genmake_version_get

from genmake.core import _author_get
from genmake.core import _basepath_find
from genmake.core import _conf_doc_prompt
from genmake.core import _conf_edit
from genmake.core import _conf_spawn
from genmake.core import _doc_create
from genmake.core import _doxyfile_generate
from genmake.core import _doxyfile_attr_match
from genmake.core import _license_sign

from genmake.core import __author__
from genmake.core import __email__
from genmake.core import __license__
from genmake.core import __maintainer__
from genmake.core import __version__
