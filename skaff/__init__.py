#!/usr/bin/env python3

__all__ = ["clitools", "config", "core"]

# To keep older scripts who import this from breaking -- DEPRECATED
from skaff.clitools import single_keypress_read
from skaff.clitools import timeout
from skaff.clitools import ANSIColor
from skaff.clitools import TimeOutError
from skaff.config import SkaffConfig
from skaff.core import skaff
from skaff.core import skaff_version_get

from skaff.core import _arguments_check
from skaff.core import _basepath_find
from skaff.core import _conf_doc_prompt
from skaff.core import _conf_edit
from skaff.core import _conf_spawn
from skaff.core import _doc_create
from skaff.core import _doxyfile_generate
from skaff.core import _doxyfile_attr_match
from skaff.core import _license_sign

from skaff.core import __author__
from skaff.core import __email__
from skaff.core import __license__
from skaff.core import __maintainer__
from skaff.core import __version__
