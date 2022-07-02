# Copyright (c) 2022-present, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import logging
import platform
import warnings
from importlib.util import find_spec

import kasai

_log = logging.getLogger(__name__)

BANNER = r"""
       {r}    )
       {r} ( /(     )         )  (
       {r} )\()) ( /(  (   ( /(  )\
       {o}((_)\  )(_)) )\  )(_))((_)
       {o}| |(_)((_)_ ((_)((_)_  (_)
       {y}| / / / _` |(_-</ _` | | |{x}
hikari-{y}|_\_\ \__,_|/__/\__,_| |_|{x}
""".format(
    r="\33[38;5;1m",
    o="\33[38;5;208m",
    y="\33[38;5;3m",
    x="\33[0m",
)


def _install_location() -> str:
    spec = find_spec("kasai")

    if spec:
        if spec.submodule_search_locations:
            return spec.submodule_search_locations[0]

    return "unknown"


def display_splash() -> None:
    print(
        BANNER + "\n"
        f"\33[3m{kasai.__description__}\33[0m\n\n"
        f"You're using version \33[1m{kasai.__version__}\33[0m.\n\n"
        f"\33[1m\33[38;5;1mInformation:\33[0m\n"
        f" • Python version: {platform.python_version()} "
        f"({platform.python_implementation()})\n"
        f" • Operating system: {platform.system()} ({platform.release()})\n"
        f" • Installed in: {_install_location()}\n\n"
        f"\33[1m\33[38;5;208mUseful links:\33[0m\n"
        f" • Documentation: \33[4m{kasai.__docs__}\33[0m\n"
        f" • Source: \33[4m{kasai.__url__}\33[0m\n"
        f" • Changelog: \33[4m{kasai.__changelog__}\33[0m\n\n"
        f"\33[1m\33[38;5;3mThanks for using kasai!\33[0m"
    )


def warn(message: str) -> None:
    if _log.hasHandlers() and _log.getEffectiveLevel() <= 30:
        _log.warning(message)
    else:
        warnings.warn(message)
