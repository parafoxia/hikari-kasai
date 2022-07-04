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

__all__ = ("IrcClient",)

import asyncio
import logging
import socket

import kasai
from kasai import ux

_log = logging.getLogger(__name__)


class IrcClient:
    """A client for IRC operations. This never needs to be created
    manually, as it will be automatically attached to your bot.
    """

    __slots__ = ("bot", "_token", "channel", "nickname", "_sock", "_task")

    def __init__(
        self, bot: kasai.GatewayApp, token: str, channel: str, nickname: str
    ) -> None:
        self.bot = bot
        self._token = token.strip()
        self.channel = channel
        self.nickname = nickname

        self._sock: socket.socket | None = None
        self._task: asyncio.Task[None] | None = None

    @property
    def is_alive(self) -> bool:
        """Whether the client is connected to a Twitch channel.

        Returns:
            :obj:`bool`
        """

        return self._sock is not None

    def _create_sock(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(False)

    async def _listen(self, loop: asyncio.AbstractEventLoop) -> None:
        assert self._sock

        while True:
            resp = await loop.sock_recv(self._sock, 512)

            if resp.startswith(b"PING"):
                await loop.sock_sendall(self._sock, b"PONG :tmi.twitch.tv\r\n")
                _log.debug("PING received, sending PONG back")

            if b"353" in resp:
                _log.info(f"joined {self.channel}")

            if b"PRIVMSG" not in resp:
                continue

            data = resp.decode("utf-8").strip()
            _log.debug(f"received message: {data}")
            self.bot.dispatch(
                kasai.IrcMessageCreateEvent(
                    message=kasai.Message.parse(data), app=self.bot
                )
            )

    @ux.deprecated("0.4a", "GatewayApp.start_irc")
    async def start(self) -> None:
        await self.bot.start_irc()

    @ux.deprecated("0.4a", "GatewayApp.close_irc")
    async def close(self) -> None:
        await self.bot.close_irc()

    async def create_message(self, content: str) -> kasai.Message:
        """Send a message to your channel's chat.

        Args:
            content:
                The content of the message. The maximum allowed message
                length varies on a number of factors, but generally,
                messages should not be longer than about 400 characters.

        Returns:
            :obj:`kasai.messages.Message`
                An object containing message information.

        Raises:
            :obj:`kasai.errors.NotConnected`:
                The client is not connected to a Twitch channel.
        """

        if self._sock is None:
            raise kasai.NotConnected("no active connections to send a message to")

        message = kasai.Message(
            self.nickname,
            self.nickname,
            f"{self.nickname}.tmi.twitch.tv",
            "PRIVMSG",
            self.channel,
            content,
        )
        loop = asyncio.get_event_loop()
        await loop.sock_sendall(self._sock, message.as_formatted.encode())
        self.bot.dispatch(kasai.IrcMessageCreateEvent(message=message, app=self.bot))
        return message
