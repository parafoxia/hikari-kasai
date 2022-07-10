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

__all__ = ("PrivMessage", "JoinMessage", "PartMessage", "ModActionMessage")

import datetime as dt
import enum
import re

import attr

import kasai
from kasai.users import UserType

_PRIV_PATTERN = re.compile(r":[^#]*([^ ]*) :(.*)")


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class PrivMessage:
    """A dataclass representing a PRIVMSG message. All attributes must
    be passed to the constructor on creation, though you should never
    need to create this yourself.
    """

    id: str
    """The message's unique ID."""

    author: kasai.User
    """The author of the message."""

    channel: kasai.Channel
    """The channel the message was sent in."""

    created_at: dt.datetime
    """The date and time the message was sent."""

    bits: int
    """The number of bits cheered in the message."""

    content: str
    """The content of the message."""

    @classmethod
    def new(cls, data: str) -> PrivMessage:
        """Create a new instance from raw (decoded) message data.

        .. note::
            The message data *must* be decoded before being passed.

        Parameters
        ----------
        data : builtins.str
            The raw (decoded) message data.

        Returns
        -------
        kasai.messages.PrivMessage
        """

        tags, message = data[1:].split(" ", maxsplit=1)
        match = _PRIV_PATTERN.match(message)
        assert match
        channel, content = match.groups()

        attrs = {(kv := attr.split("="))[0]: kv[1] for attr in tags.split(";")}

        return cls(
            id=attrs["id"],
            author=kasai.User(
                id=attrs["user-id"],
                color=int(attrs["color"][1:] or "0", base=16),
                display_name=attrs["display-name"],
                is_mod=bool(int(attrs["mod"])),
                is_subscriber=bool(int(attrs["subscriber"])),
                is_turbo=bool(int(attrs["turbo"])),
                is_broadcaster="broadcaster" in attrs["badges"],
                type=UserType(attrs["user-type"]),
            ),
            channel=kasai.Channel(
                id=attrs["room-id"],
                name=channel,
            ),
            created_at=dt.datetime.fromtimestamp(int(attrs["tmi-sent-ts"]) / 1000),
            bits=int(attrs.get("bits", 0)),
            content=content,
        )


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class JoinMessage:
    """A dataclass representing a JOIN message. All attributes must be
    passed to the constructor on creation, though you should never need
    to create this yourself.
    """

    channel_name: str
    """The name of the channel which was joined."""

    @classmethod
    def new(cls, data: str) -> JoinMessage:
        """Create a new instance from raw (decoded) message data.

        .. note::
            The message data *must* be decoded before being passed.

        Parameters
        ----------
        data : builtins.str
            The raw (decoded) message data.

        Returns
        -------
        kasai.messages.JoinMessage
        """

        channel = data.split()[-1]
        return cls(channel_name=channel)


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class PartMessage:
    """A dataclass representing a PART message. All attributes must be
    passed to the constructor on creation, though you should never need
    to create this yourself.
    """

    channel_name: str
    """The name of the channel which was joined."""

    @classmethod
    def new(cls, data: str) -> PartMessage:
        """Create a new instance from raw (decoded) message data.

        .. note::
            The message data *must* be decoded before being passed.

        Parameters
        ----------
        data : builtins.str
            The raw (decoded) message data.

        Returns
        -------
        kasai.messages.PartMessage
        """

        channel = data.split()[-1]
        return cls(channel_name=channel)


class ModCommandType(enum.Enum):
    CLEAR = 0
    BAN = 1
    TIMEOUT = 2


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class ModActionMessage:
    """A dataclass representing a CLEARCHAT message. All attributes must
    be passed to the constructor on creation, though you should never
    need to create this yourself.

    .. important::
        This is triggered whenever a mod in your chat executes one of
        the following moderation actions:

        * /clear
        * /ban
        * /timeout

        This is always sent as a CLEARCHAT message regardless of the
        action taken. Action reasons are also not collected by this
        class.
    """

    target_id: str | None
    """The target user's ID. This is `None` if a clear command was
    sent."""

    channel: kasai.Channel
    """The channel the command was executed in."""

    created_at: dt.datetime
    """The time the command was executed."""

    command: ModCommandType
    """The command that was executed."""

    duration: int
    """The duration of the action. This is only non-zero if the command
    was a timeout, in which case it will be the number of seconds the
    user is timed out for."""

    @classmethod
    def new(cls, data: str) -> ModActionMessage:
        """Create a new instance from raw (decoded) message data.

        .. note::
            The message data *must* be decoded before being passed.

        Parameters
        ----------
        data : builtins.str
            The raw (decoded) message data.

        Returns
        -------
        kasai.messages.ModActionMessage
        """

        tags, message = data[1:].split(" ", maxsplit=1)
        channel = message.split()[2]

        attrs = {(kv := attr.split("="))[0]: kv[1] for attr in tags.split(";")}
        keys = attrs.keys()

        if "ban-duration" in keys:
            cmd = ModCommandType.TIMEOUT
        elif "target-user-id" in keys:
            cmd = ModCommandType.BAN
        else:
            cmd = ModCommandType.CLEAR

        return cls(
            target_id=attrs.get("target-user-id", None),
            channel=kasai.Channel(
                id=attrs["room-id"],
                name=channel,
            ),
            created_at=dt.datetime.fromtimestamp(int(attrs["tmi-sent-ts"]) / 1000),
            command=cmd,
            duration=int(attrs.get("ban-duration", 0)),
        )
