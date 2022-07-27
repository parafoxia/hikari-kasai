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

__all__ = (
    "KasaiError",
    "NotAlive",
    "IsAlive",
    "HelixError",
    "RequestFailed",
    "IrcError",
    "NotJoined",
)


class KasaiError(Exception):
    """The base exception class for all Kasai errors."""


class NotAlive(KasaiError):
    """Exception thrown when the Twitch client is not alive when it
    should be."""


class IsAlive(KasaiError):
    """Exception thrown when the Twitch client is alive when it
    shouldn't be."""


class HelixError(KasaiError):
    """Exception thrown when something goes wrong regarding the Twitch
    Helix API."""


class RequestFailed(HelixError):
    """Exception thrown when a Twitch Helix API request fails."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")


class IrcError(KasaiError):
    """Exception thrown when something goes wrong regarding IRC."""


class NotJoined(IrcError):
    """Exception thrown when sending a message to a channel the client
    has not joined."""
