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

__all__ = ("TwitchClient",)

import asyncio
import logging
import socket
from hashlib import sha256
from time import time

import kasai

_log = logging.getLogger(__name__)


class TwitchClient:
    """A class for interacting with Twitch. This is available through
    :obj:`kasai.bot.GatewayBot.twitch`, and should never need to be
    manually instantiated.

    Args:
        bot:
            The bot instance.
        token:
            Your Twitch IRC token

    Attributes:
        bot (:obj:`kasai.bot.GatewayBot`):
            The bot instance.
    """

    __slots__ = ("bot", "_token", "_nickname", "_channels", "_sock", "_task")

    def __init__(self, bot: kasai.GatewayBot, token: str) -> None:
        self.bot = bot
        self._token = token
        self._nickname = sha256(f"{time()}".encode("utf-8")).hexdigest()[:7]
        self._channels: list[str] = []
        self._sock: socket.socket | None = None
        self._task: asyncio.Task[None] | None = None

    @property
    def is_alive(self) -> bool:
        """Whether the websocket is open. This does not necessarily mean
        it's connected to a channel.

        Returns:
            :obj:`bool`
        """

        return self._sock is not None

    @property
    def channels(self) -> list[str]:
        """A list of channels the client is connected to.

        Returns:
            :obj:`list` [:obj:`str`]

        .. versionadded:: 0.5a
        """

        return self._channels

    def _create_sock(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(False)

    async def _irclisten(self, loop: asyncio.AbstractEventLoop) -> None:
        assert self._sock

        while True:
            resp = await loop.sock_recv(self._sock, 512)
            data = resp.decode("utf-8").strip()
            _log.debug(f"received IRC message: {data}")

            if resp.startswith(b"PING"):
                await loop.sock_sendall(self._sock, b"PONG :tmi.twitch.tv\r\n")
                self.bot.dispatch(kasai.PingEvent(app=self.bot))
                continue

            if b"JOIN" in resp:
                join = kasai.JoinMessage.new(data)
                self.bot.dispatch(kasai.JoinEvent(message=join, app=self.bot))
                self._channels.append(join.channel_name)
                _log.info(f"joined {join.channel_name}")
                continue

            if b"PART" in resp:
                part = kasai.PartMessage.new(data)
                self.bot.dispatch(kasai.PartEvent(message=part, app=self.bot))
                self._channels.remove(part.channel_name)
                _log.info(f"parted {part.channel_name}")
                continue

            if b"PRIVMSG" not in resp:
                continue

            pm = kasai.PrivMessage.new(data)
            self.bot.dispatch(kasai.PrivMessageCreateEvent(message=pm, app=self.bot))

    async def join(self, *channels: str) -> None:
        """Join a Twitch channel.

        Args:
            *channels:
                The channels to join. This can be empty, in which case,
                nothing will happen.

        Raises:
            :obj:`kasai.errors.NotConnected`:
                The client is not connected to Twitch.

        .. versionadded:: 0.4a
        """

        if self._sock is None:
            raise kasai.NotConnected("no active connections")

        if not channels:
            return

        loop = asyncio.get_running_loop()
        msg = "\r\n".join(f"JOIN {c}" for c in channels) + "\r\n"
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))

    async def part(self, *channels: str) -> None:
        """Part (or leave) a Twitch channel.

        Args:
            *channels:
                The channels to part. This can be empty, in which case,
                nothing will happen.

        Raises:
            :obj:`kasai.errors.NotConnected`:
                The client is not connected to Twitch.

        .. versionadded:: 0.4a
        """

        if self._sock is None:
            raise kasai.NotConnected("no active connections")

        loop = asyncio.get_running_loop()
        msg = "\r\n".join(f"PART {c}" for c in channels) + "\r\n"
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))

    async def create_message(self, channel: str, content: str) -> None:
        """Send a message to a given channel's chat. The client must
        have joined that channel to send a message.

        Args:
            channel:
                The channel to send the message to. This must be
                prefixed with a hash (#).
            content:
                The content of the message. The maximum allowed message
                length varies on a number of factors, but generally,
                messages should not be longer than about 400 characters.

        Raises:
            :obj:`kasai.errors.NotConnected`:
                The client is not connected to a Twitch channel.
        """

        if self._sock is None:
            raise kasai.NotConnected("no active connections to send a message to")

        msg = (
            f":{self._nickname}!{self._nickname}@{self._nickname}.tmi.twitch.tv "
            f"PRIVMSG {channel} {content}\r\n"
        )
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))
