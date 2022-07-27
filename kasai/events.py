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
    "MessageCreateEvent",
    "PingEvent",
    "JoinEvent",
    "PartEvent",
    "JoinRoomstateEvent",
    "ModActionEvent",
    "ClearEvent",
    "BanEvent",
    "TimeoutEvent",
)

import abc
import datetime as dt

import attr
from hikari import Event
from hikari.internal import attr_extensions

import kasai


class KasaiEvent(Event, abc.ABC):
    """The basis for all Kasai events."""

    @property
    @abc.abstractmethod
    def app(self) -> kasai.TwitchAware:
        """The bot client instance."""


@attr.define(kw_only=True, weakref_slot=False)
class MessageCreateEvent(KasaiEvent):
    """Event fired when a Twitch IRC message is sent.

    .. important::
        This event is not triggered when your bot sends a message.
    """

    message: kasai.Message = attr.field()
    """The message that was sent."""

    @property
    def message_id(self) -> str:
        """The ID of the sent message."""
        return self.message.id

    @property
    def app(self) -> kasai.TwitchAware:
        """The base client application."""
        return self.message.app

    @property
    def author(self) -> kasai.Viewer:
        """The user who sent the message."""
        return self.message.author

    @property
    def author_id(self) -> str:
        """The ID of the user who sent the message."""
        return self.message.author.id

    @property
    def channel(self) -> kasai.Channel:
        """The channel the message was sent to."""
        return self.message.channel

    @property
    def channel_id(self) -> str:
        """The ID of the channel the message was sent to."""
        return self.message.channel.id

    @property
    def bits(self) -> int:
        """The number of bits the user sent in the message."""
        return self.message.bits

    @property
    def content(self) -> str:
        """The text content of the message."""
        return self.message.content


@attr.define(kw_only=True, weakref_slot=False)
class PingEvent(KasaiEvent):
    """Event fired when the client receives a PING message."""

    app: kasai.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    """The base client application."""


@attr.define(kw_only=True, weakref_slot=False)
class JoinEvent(KasaiEvent):
    """Event fired when the client joins a Twitch channel's chat.

    .. important::
        To get more information about the channel, use
        `JoinRoomstateEvent` instead.
    """

    channel: str = attr.field()
    """The name of the channel the client joined."""

    app: kasai.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    """The base client application."""


@attr.define(kw_only=True, weakref_slot=False)
class PartEvent(KasaiEvent):
    """Event fired when the client parts (leaves) a Twitch channel's
    chat."""

    channel: str = attr.field()
    """The name of the channel the client parted."""

    app: kasai.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )


@attr.define(kw_only=True, weakref_slot=False)
class JoinRoomstateEvent(KasaiEvent):
    """Event fired when the client receives ROOMSTATE information after
    joining a channel.

    .. note::
        This event contains more detailed information regarding the
        channel the client joined, however as that information does not
        always get sent from Twitch immediately, it is dispatched with
        a separate event.
    """

    channel: kasai.Channel = attr.field()
    """The channel the client joined."""

    @property
    def channel_id(self) -> str:
        """The ID of the channel the client joined."""
        return self.channel.id

    @property
    def app(self) -> kasai.TwitchAware:
        """The base client instance."""
        return self.channel.app

    @property
    def game(self) -> kasai.Game:
        """The game the channel is currently playing (or most recently
        played)."""
        return self.channel.game

    @property
    def game_id(self) -> str:
        """The ID of the game the channel is currently playing (or most
        recently played)."""
        return self.channel.game.id

    @property
    def title(self) -> str:
        """The title of the channel's current (or most recent)
        stream."""
        return self.channel.title


@attr.define(kw_only=True, weakref_slot=False)
class ModActionEvent(KasaiEvent):
    """Event fired when a moderation action is taken.

    .. note::
        This currently only supports CLEARCHAT, BAN, and TIMEOUT
        actions.
    """

    channel: kasai.Channel = attr.field()
    """The channel the mod action was performed in."""

    created_at: dt.datetime = attr.field()
    """The date and time the mod action was executed."""

    @property
    def channel_id(self) -> str:
        """The ID of the channel."""
        return self.channel.id

    @property
    def app(self) -> kasai.TwitchAware:
        """The base client instance."""
        return self.channel.app


@attr.define(kw_only=True, weakref_slot=False)
class ClearEvent(ModActionEvent):
    """Event fired when a chat is cleared."""


@attr.define(kw_only=True, weakref_slot=False)
class BanEvent(ModActionEvent):
    """Event fired when a user is banned from a chat channel."""

    user: kasai.User = attr.field()
    """The user that was banned."""

    @property
    def user_id(self) -> str:
        """The ID of the user that was banned."""
        return self.user.id


@attr.define(kw_only=True, weakref_slot=False)
class TimeoutEvent(ModActionEvent):
    """Event fired when a user is timed out from a chat channel."""

    user: kasai.User = attr.field()
    """The user that was banned."""

    duration: int = attr.field()
    """The duration of the timeout, in seconds."""

    @property
    def user_id(self) -> str:
        """The ID of the user that was banned."""
        return self.user.id
