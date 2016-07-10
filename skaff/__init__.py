#!/usr/bin/env python3

# ------------------------------- MODULE INFO ---------------------------------
# Note the naming convention shown here coming from the 'ranger' program from
# http://ranger.nongnu.org/
__all__ = ["clitools", "config", "core"]
__author__ = "Jiahui Xie"
__email__ = "jiahui.xie@outlook.com"
__license__ = "BSD2"
__maintainer__ = __author__
__version__ = "1.0"
# ------------------------------- MODULE INFO ---------------------------------

# To keep older scripts who import this from breaking -- DEPRECATED
from skaff.clitools import getkey
from skaff.clitools import timeout
from skaff.clitools import ANSIColor
from skaff.clitools import TimeOutError
from skaff.config import SkaffConfig
from skaff.core import skaff
from skaff.core import skaff_version_get

from skaff.core import _arguments_check
from skaff.core import _conf_doc_prompt
from skaff.core import _conf_edit
from skaff.core import _conf_spawn
from skaff.core import _doc_create
from skaff.core import _doxyfile_generate
from skaff.core import _doxyfile_attr_match
from skaff.core import _license_sign
