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

import datetime as dt

import attr
from hikari.internal import attr_extensions

import kasai
from kasai import traits


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class Message:
    """A class representing a Twitch IRC PRIVMSG."""

    app: traits.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    """The base client application."""

    id: str = attr.field(hash=True, repr=True)
    """This message's ID."""

    author: kasai.Viewer = attr.field(eq=False, hash=False, repr=True)
    """The user who sent this message."""

    channel: kasai.Channel = attr.field(eq=False, hash=False, repr=True)
    """The channel this message was sent to.."""

    created_at: dt.datetime = attr.field(eq=False, hash=False, repr=True)
    """The date and time this message was sent."""

    bits: int = attr.field(eq=False, hash=False, repr=True)
    """The number of bits the user sent in this message."""

    content: str = attr.field(eq=False, hash=False, repr=True)
    """The text content of this message."""

    async def respond(self, content: str, *, reply: bool = False) -> None:
        """Sends a message to this channel this message was sent to.

        Example
        -------
        ```py
        >>> await message.respond("Never gonna give you up!")
        ```

        Example
        -------
        ```py
        >>> await message.respond(
            "Never gonna let you down!",
            reply=True,
        )
        ```

        Parameters
        ----------
        content : str
            The text content of the message you want to send.

        Other Parameters
        ----------------
        reply : bool
            Whether to send the message in reply to this one. Defaults
            to `False`.

            .. versionadded:: 0.8a

        Returns
        -------
        None
        """

        await self.app.twitch.create_message(
            self.channel.username, content, reply_to=self.id if reply else None
        )
