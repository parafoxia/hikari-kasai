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

__all__ = ("KasaiEvent", "IrcMessageCreateEvent")

import typing as t

import attr
from hikari import Event
from hikari.internal import attr_extensions

if t.TYPE_CHECKING:
    from hikari import traits

    from kasai.messages import Message


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class KasaiEvent(Event):
    """A dataclass representing a Kasai event. All instance attributes
    must be passed to the constructor on creation.
    """

    app: traits.RESTAware = attr.field(metadata={attr_extensions.SKIP_DEEP_COPY: True})
    """The bot client instance."""


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class IrcMessageCreateEvent(KasaiEvent):
    """A dataclass created whenever the IRC client receives a new Twitch
    chat message. All instance attributes must be passed to the
    constructor on creation.
    """

    message: Message
    """The received message."""

    @property
    def user(self) -> str:
        """The message author's username.

        Returns:
            :obj:`str`
        """

        return self.message.user

    @property
    def channel(self) -> str:
        """The channel the message was sent to.

        Returns:
            :obj:`str`
        """

        return self.message.channel

    @property
    def content(self) -> str:
        """The content of the message.

        Returns:
            :obj:`str`
        """

        return self.message.content
