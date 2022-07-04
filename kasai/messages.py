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

__all__ = ("Message",)

import re

import attr

# https://datatracker.ietf.org/doc/html/rfc2812.html#section-2.3
_PATTERN = re.compile(r":([^!]*)!([^@]*)@([^ ]*) ([^ ]*) ([^ ]*) :(.*)")


@attr.define(hash=True, weakref_slot=False)
class Message:
    """A dataclass representing a message. All instance attributes must
    be passed to the constructor on creation."""

    nickname: str
    """The message author's nickname."""

    user: str
    """The message author's username."""

    host: str
    """The message author's host."""

    type: str
    """The message type."""

    channel: str
    """The channel the message was sent to."""

    content: str
    """The content of the message."""

    @classmethod
    def parse(cls, message: str) -> Message:
        """Create a new instance from a raw IRC message.

        .. note::
            The message must be decoded before passing it through.

        Args:
            message:
                The decoded IRC message.

        Returns:
            The newly created message.
        """

        if match := _PATTERN.match(message):
            return cls(*match.groups())
        else:
            return cls(*(["unknown"] * 6))

    @property
    def as_formatted(self) -> str:
        """Return an instance in a IRC message format.

        .. note::
            This must be encoded before sending the message over IRC.

        Returns:
            :obj:`str`
        """

        return (
            f":{self.nickname}!{self.user}@{self.host} "
            f"{self.type} {self.channel} :{self.content}\r\n"
        )
