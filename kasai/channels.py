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

__all__ = ("Channel",)

import typing as t

import attr
from hikari.internal import attr_extensions

from kasai import traits

if t.TYPE_CHECKING:
    import kasai


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class Channel:
    """A class representing a Twitch channel."""

    app: traits.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    """The base client application."""

    id: str = attr.field(hash=True, repr=True)
    """This channel's ID."""

    username: str = attr.field(eq=False, hash=False, repr=False)
    """This channel's login username."""

    display_name: str = attr.field(eq=False, hash=False, repr=True)
    """The name this channel is displayed as on Twitch. This will always
    be the username with casing variations."""

    language: str = attr.field(eq=False, hash=False, repr=False)
    """The language this channel is streaming using (according to their
    settings)."""

    game: kasai.Game = attr.field(eq=False, hash=False, repr=True)
    """The game this channel is playing."""

    title: str = attr.field(eq=False, hash=False, repr=True)
    """The title of this channel's stream."""

    delay: int = attr.field(eq=False, hash=False, repr=False)
    """The number of seconds this channel's stream is delayed by."""

    @property
    def irc_format(self) -> str:
        """This channel's username in the format IRC expects it."""

        return f"#{self.username}"

    async def send(self, content: str) -> None:
        """Send a message to this channel.

        Example
        -------
        ```py
        >>> await channel.send("Never gonna give you up!")
        ```

        Parameters
        ----------
        content : str
            The text content of the message you want to send.

        Returns
        -------
        None
        """

        await self.app.twitch.create_message(self.username, content)
