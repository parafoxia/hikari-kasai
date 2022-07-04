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

__all__ = ("User",)

import enum

import attr


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


@attr.define(hash=True, kw_only=True, weakref_slot=False)
class User:
    """A dataclass representing a Twitch user. All attributes must be
    passed to the constructor on creation, though you should never need
    to create this yourself.

    .. note::
        This does not necessarily represent a global user. The values
        of some attributes are dependent on context, often the channel
        the user was in when they sent a message.
    """

    id: str
    """The user's ID."""

    color: int
    """The user's colour in the current context. This is an integer
    representation of the colour's hex code."""

    display_name: str
    """The user's display name."""

    is_mod: bool
    """Whether the user is a mod in the current context."""

    is_subscriber: bool
    """Whether the user is a subscriber in the current context."""

    is_turbo: bool
    """Whether the user has ads turned off globally."""

    is_broadcaster: bool
    """Whether the user is the broadcaster."""

    type: UserType
    """The user type. This will be :obj:`UserType.NORMAL` unless the
    user works for Twitch."""

    @property
    def username(self) -> str:
        """The user's username. This is always their display name in
        all lower case.

        Returns:
            :obj:`str`
        """

        return self.display_name.lower()

    @property
    def colour(self) -> int:
        """An alias for those who can spell correctly. This is an
        integer representation of the colour's hex code.

        Return:
            :obj:`int`
        """

        return self.color
