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

__all__ = ("Stream", "StreamType")

import datetime as dt
import enum

import attr
from dateutil.tz import tzutc
from hikari.internal import attr_extensions

import kasai
from kasai import traits


class StreamType(enum.Enum):
    """An enum representing a stream type."""

    LIVE = "live"
    """Represents a live stream. This should also be the case."""

    UNKNOWN = ""
    """Only occurs when an error occurs."""


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class Stream:
    """A class representing a Twitch stream."""

    app: traits.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    """The base client application."""

    id: str = attr.field(hash=True, repr=True)
    """This stream's ID."""

    channel: kasai.Channel = attr.field(eq=False, hash=False, repr=True)
    """The channel this stream is being broadcast to."""

    type: StreamType = attr.field(eq=False, hash=False, repr=False)
    """The stream type. This should always be `StreamType.LIVE` though
    can be `StreamType.UNKNOWN` in the case of an error."""

    viewer_count: int = attr.field(eq=False, hash=False, repr=True)
    """The number of viewers watching this stream at the time the
    request was made."""

    created_at: dt.datetime = attr.field(eq=False, hash=False, repr=True)
    """The date and time this stream started."""

    is_mature: bool = attr.field(eq=False, hash=False, repr=True)
    """Whether this stream is marked as mature (18+)."""

    thumbnail_url: str = attr.field(eq=False, hash=False, repr=False)
    """The raw thumbnail URL."""

    @property
    def uptime(self) -> dt.timedelta:
        """The amount of time the stream has been live."""

        return dt.datetime.now(tz=tzutc()) - self.created_at

    def get_thumbnail_url(self, width: int, height: int) -> str:
        """Get the thumbnail URL for a specific width and height.

        Example
        -------
        ```py
        >>> stream.get_thumbnail_url(1280, 720)
        ```

        Parameters
        ----------
        width : int
            The thumbnail width, in pixels.
        height : int
            The thumbnail height, in pixels.

        Returns
        -------
        str
            The formatted thumbnail URL.
        """

        return self.thumbnail_url.format(width=width, height=height)
