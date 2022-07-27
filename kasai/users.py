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

__all__ = ("User", "Viewer")

import abc
import datetime as dt
import enum

import attr
from hikari.internal import attr_extensions

from kasai import traits


class UserType(enum.Enum):
    """An enum representing a user type."""

    NORMAL = ""
    """"""
    ADMIN = "admin"
    """"""
    GLOBAL_MOD = "global_mod"
    """"""
    STAFF = "staff"
    """"""


class User(abc.ABC):
    """A class representing a Twitch user."""

    __slots__ = ()

    @property
    @abc.abstractmethod
    def app(self) -> traits.TwitchAware:
        """Client application that models may use for procedures."""

    @property
    @abc.abstractmethod
    def broadcaster_type(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def display_name(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def username(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def offline_image_url(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def profile_image_url(self) -> str:
        """A property."""

    @property
    @abc.abstractmethod
    def type(self) -> UserType:
        """A property."""

    @property
    @abc.abstractmethod
    def created_at(self) -> dt.datetime:
        """A property."""


class Viewer(User, abc.ABC):
    """A class representing a Twitch viewer.

    This is largely the same as a normal `User`, but contains additional
    information related to the user's relationship with the channel
    they're currently viewing.
    """

    @property
    @abc.abstractmethod
    def color(self) -> int:
        """A property."""

    @property
    def colour(self) -> int:
        """A property."""
        return self.color

    @property
    @abc.abstractmethod
    def is_mod(self) -> bool:
        """A property."""

    @property
    @abc.abstractmethod
    def is_subscriber(self) -> bool:
        """A property."""

    @property
    @abc.abstractmethod
    def is_turbo(self) -> bool:
        """A property."""

    @property
    @abc.abstractmethod
    def is_broadcaster(self) -> bool:
        """A property."""


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
    """The client application that models may use for procedures."""

    broadcaster_type: str = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    description: str = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    display_name: str = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""

    id: str = attr.field(hash=True, repr=True)
    """The ID of this user."""

    username: str = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    offline_image_url: str = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    profile_image_url: str = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    type: UserType = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    created_at: dt.datetime = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""

    def __str__(self) -> str:
        return self.username


@attr_extensions.with_copy
@attr.define(hash=True, kw_only=True, weakref_slot=False)
class ViewerImpl(UserImpl, Viewer):
    """Concrete implementation of viewer information."""

    color: int = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""

    is_mod: bool = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""

    is_subscriber: bool = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""

    is_turbo: bool = attr.field(eq=False, hash=False, repr=False)
    """An attribute."""

    is_broadcaster: bool = attr.field(eq=False, hash=False, repr=True)
    """An attribute."""
