#!/usr/bin/env python3

"""
A collection of extensible tools used for project scaffolding that comes with
default C/C++ support.
"""

# -------------------------------- COPYRIGHT ----------------------------------
# Copyright © 2016 Jiahui Xie
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# -------------------------------- COPYRIGHT ----------------------------------

# ------------------------------- MODULE INFO ---------------------------------
# Note the naming convention shown here coming from the 'ranger' program from
# http://ranger.nongnu.org/
__all__ = ["clitools", "config", "driver", "manualtools"]
__author__ = "Jiahui Xie"
__email__ = "jiahui.xie@outlook.com"
__license__ = "BSD2"
__maintainer__ = __author__
__version__ = "1.0"
# ------------------------------- MODULE INFO ---------------------------------

# To keep older "one level import statements" like
# "
# from skaff import getkey
# "
# (only used in 'driver_test' unit test module to access private functions)
# from breaking -- DEPRECATED
from skaff.clitools import getkey
from skaff.clitools import timeout
from skaff.clitools import ANSIColor
from skaff.clitools import TimeOutError
from skaff.clitools import SmartFormatter

from skaff.config import SkaffConfig

from skaff.driver import skaff_drive
from skaff.driver import skaff_version_get
from skaff.driver import _arguments_check
from skaff.driver import _conf_doc_prompt
from skaff.driver import _conf_edit
from skaff.driver import _conf_spawn
from skaff.driver import _doc_create
from skaff.driver import _doxyfile_generate
from skaff.driver import _doxyfile_attr_match
from skaff.driver import _license_sign

from skaff.manualtools import manual_check
from skaff.manualtools import manuals_install
from skaff.manualtools import manuals_probe
from skaff.manualtools import manpath_select
