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

__all__ = ("User", "Viewer", "UserType", "BroadcasterType")

import abc
import datetime as dt
import enum

import attr
from hikari.internal import attr_extensions

from kasai import traits


class UserType(enum.Enum):
    """An enum representing a user type."""

    NORMAL = ""
    """Represents a normal user."""

    ADMIN = "admin"
    """Represents a Twitch admin."""

    GLOBAL_MOD = "global_mod"
    """Represents a global mod."""

    STAFF = "staff"
    """Represents a Twitch staff member."""


class BroadcasterType(enum.Enum):
    """An enum representing a broadcaster type.

    .. versionadded:: 0.8a
    """

    NORMAL = ""
    """Represents a normal broadcaster."""

    AFFILIATE = "affiliate"
    """Represents an affiliated broadcaster."""

    PARTNER = "partner"
    """Represents a partnered broadcaster."""


class User(abc.ABC):
    """A class representing a Twitch user."""

    __slots__ = ()

    @property
    @abc.abstractmethod
    def app(self) -> traits.TwitchAware:
        """The base client application."""

    @property
    @abc.abstractmethod
    def broadcaster_type(self) -> BroadcasterType:
        """This user's broadcaster type.

        This can be:

        - `BroadcasterType.NORMAL`
        - `BroadcasterType.AFFILIATE`
        - `BroadcasterType.PARTNER`

        .. versionchanged:: 0.8a
            This is now an enum rather than a string.
        """

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """This user's channel description."""

    @property
    @abc.abstractmethod
    def display_name(self) -> str:
        """The name this user displays as on Twitch."""

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """This user's ID."""

    @property
    @abc.abstractmethod
    def username(self) -> str:
        """This user's login username."""

    @property
    def login(self) -> str:
        """A helper property which provides this username using Twitch
        naming conventions.

        .. versionadded:: 0.8a
        """
        return self.username

    @property
    @abc.abstractmethod
    def offline_image_url(self) -> str:
        """The URL of this user's channel's offline image."""

    @property
    @abc.abstractmethod
    def profile_image_url(self) -> str:
        """The URL of this user's profile image."""

    @property
    @abc.abstractmethod
    def type(self) -> UserType:
        """This user's type.

        This can be:

        - `UserType.NORMAL`
        - `UserType.ADMIN`
        - `UserType.GLOBAL_MOD`
        - `UserType.STAFF`
        """

    @property
    @abc.abstractmethod
    def created_at(self) -> dt.datetime:
        """The date and time this user created their account."""


class Viewer(User, abc.ABC):
    """A class representing a Twitch viewer.

    This is largely the same as a normal `User`, but contains additional
    information related to the user's relationship with the channel
    they're currently viewing.
    """

    @property
    @abc.abstractmethod
    def color(self) -> int:
        """The colour this user uses in the channel's chat."""

    @property
    def colour(self) -> int:
        """An alias for the good ol' Bri'ish. And people who can
        spell."""
        return self.color

    @property
    @abc.abstractmethod
    def is_mod(self) -> bool:
        """Whether this user is a mod in the channel."""

    @property
    @abc.abstractmethod
    def is_subscriber(self) -> bool:
        """Whether this user is a subscriber of the channel."""

    @property
    @abc.abstractmethod
    def is_turbo(self) -> bool:
        """Whether this user has ads turned off globally."""

    @property
    @abc.abstractmethod
    def is_broadcaster(self) -> bool:
        """Whether this user is the channel's broadcaster."""


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class UserImpl(User):
    """Concrete implementation of user information."""

    app: traits.TwitchAware = attr.field(
        repr=False,
        eq=False,
        hash=False,
        metadata={attr_extensions.SKIP_DEEP_COPY: True},
    )
    broadcaster_type: BroadcasterType = attr.field(eq=False, hash=False, repr=False)
    description: str = attr.field(eq=False, hash=False, repr=False)
    display_name: str = attr.field(eq=False, hash=False, repr=True)
    id: str = attr.field(hash=True, repr=True)
    username: str = attr.field(eq=False, hash=False, repr=False)
    offline_image_url: str = attr.field(eq=False, hash=False, repr=False)
    profile_image_url: str = attr.field(eq=False, hash=False, repr=False)
    type: UserType = attr.field(eq=False, hash=False, repr=False)
    created_at: dt.datetime = attr.field(eq=False, hash=False, repr=True)

    def __str__(self) -> str:
        return self.username


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class ViewerImpl(UserImpl, Viewer):
    """Concrete implementation of viewer information."""

    color: int = attr.field(eq=False, hash=False, repr=True)
    is_mod: bool = attr.field(eq=False, hash=False, repr=True)
    is_subscriber: bool = attr.field(eq=False, hash=False, repr=True)
    is_turbo: bool = attr.field(eq=False, hash=False, repr=False)
    is_broadcaster: bool = attr.field(eq=False, hash=False, repr=True)
