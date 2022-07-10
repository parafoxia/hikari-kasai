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

__all__ = (
    "KasaiEvent",
    "PrivMessageCreateEvent",
    "PingEvent",
    "JoinEvent",
    "PartEvent",
    "ClearEvent",
    "BanEvent",
    "TimeoutEvent",
)

import typing as t

import attr
from hikari import Event
from hikari.internal import attr_extensions

import kasai

if t.TYPE_CHECKING:
    from hikari import traits

    from kasai.messages import JoinMessage, ModActionMessage, PartMessage, PrivMessage


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
class PrivMessageCreateEvent(KasaiEvent):
    """A dataclass created whenever the client receives a new Twitch
    chat message. All instance attributes must be passed to the
    constructor on creation.

    .. important::
        This event is not triggered when your bot sends a message.
    """

    message: PrivMessage
    """The message that was sent."""

    @property
    def author(self) -> kasai.User:
        """The message's author.

        Returns
        -------
        kasai.users.User
        """

        return self.message.author

    @property
    def channel(self) -> kasai.Channel:
        """The channel the message was sent to.

        Returns
        -------
        kasai.channels.Channel
        """

        return self.message.channel

    @property
    def content(self) -> str:
        """The content of the message.

        Returns
        -------
        builtins.str
        """

        return self.message.content


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class PingEvent(KasaiEvent):
    """A dataclass created whenever the client receives a PING message
    from the Twitch server. All instance attributes must be passed to
    the constructor on creation.
    """


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class JoinEvent(KasaiEvent):
    """A dataclass created whenever the client joins a Twitch channel.
    All instance attributes must be passed to the constructor on
    creation.
    """

    message: JoinMessage
    """A representation of a JOIN message."""

    @property
    def channel_name(self) -> str:
        """The name of the channel which was joined.

        Returns
        -------
        builtins.str
        """

        return self.message.channel_name


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class PartEvent(KasaiEvent):
    """A dataclass created whenever the client parts a Twitch channel.
    All instance attributes must be passed to the constructor on
    creation.
    """

    message: PartMessage
    """A representation of a PART message."""

    @property
    def channel_name(self) -> str:
        """The name of the channel which was parted.

        Returns
        -------
        builtins.str
        """

        return self.message.channel_name


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class ClearEvent(KasaiEvent):
    """A dataclass created whenever a clear command is sent to the
    Twitch channel. All instance attributes must be passed to the
    constructor on creation.
    """

    message: ModActionMessage
    """A representation of a CLEARCHAT message."""


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class BanEvent(KasaiEvent):
    """A dataclass created whenever a ban command is sent to the Twitch
    channel. All instance attributes must be passed to the constructor
    on creation.
    """

    message: ModActionMessage
    """A representation of a CLEARCHAT message."""

    @property
    def target_id(self) -> str:
        """The target user's ID.

        Returns
        -------
        builtins.str
        """

        assert self.message.target_id is not None
        return self.message.target_id


@attr_extensions.with_copy
@attr.define(kw_only=True, weakref_slot=False)
class TimeoutEvent(KasaiEvent):
    """A dataclass created whenever a timeout command is sent to the
    Twitch channel. All instance attributes must be passed to the
    constructor on creation.
    """

    message: ModActionMessage
    """A representation of a CLEARCHAT message."""

    @property
    def target_id(self) -> str:
        """The target user's ID.

        Returns
        -------
        builtins.str
        """

        assert self.message.target_id is not None
        return self.message.target_id

    @property
    def duration(self) -> int:
        """The timeout duration.

        Returns
        -------
        builtins.int
        """

        return self.message.duration
