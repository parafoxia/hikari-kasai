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

import sys

__all__ = ("BANNER", "display_splash", "deprecated")

import logging
import typing as t

from hikari import cli

import kasai

_log = logging.getLogger(__name__)
_FuncT = t.Callable[..., t.Any]


def display_splash() -> None:
    sys.stderr.write(f"hikari-kasai ({kasai.__version__})\n")
    cli.main()


def depr_warn(thing: str, ver: str, resolution: str | None) -> None:
    msg = f"'{thing}' is deprecated, and will be removed in v{ver}"
    if resolution:
        msg += f" — {resolution}"
    _log.warning(msg)


def deprecated(ver: str, resolution: str | None = None) -> t.Callable[[_FuncT], _FuncT]:
    def decorator(func: _FuncT) -> _FuncT:
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            depr_warn(ver, func.__qualname__, resolution)
            return func(*args, **kwargs)

        return wrapper

    return decorator
