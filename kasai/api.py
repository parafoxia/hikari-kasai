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

from hikari import GatewayBot

import kasai

_HOST = "irc.chat.twitch.tv"
_PORT = 6667

_log = logging.getLogger(__name__)


class IrcClient:
    __slots__ = ("bot", "_token", "channel", "nickname", "_listen", "_sock", "_task")

    def __init__(
        self, bot: GatewayBot, token: str, channel: str, nickname: str
    ) -> None:
        self.bot = bot
        self._token = token.strip()
        self.channel = channel
        self.nickname = nickname

        self._sock: socket.socket | None = None
        self._task: asyncio.Task[None] | None = None
        self._listen = False

    @property
    def is_alive(self) -> bool:
        return self._sock is not None

    def _create_new_sock(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(False)

    async def start(self) -> None:
        if self._sock is not None:
            raise kasai.AlreadyConnected("there is already an active connection")

        loop = asyncio.get_running_loop()

        self._create_new_sock()
        assert self._sock is not None
        await loop.sock_connect(self._sock, (_HOST, _PORT))
        await loop.sock_sendall(
            self._sock,
            (
                f"PASS {self._token}\n"
                f"NICK {self.nickname}\n"
                f"JOIN {self.channel}\n"
            ).encode("utf-8"),
        )

        self._listen = True

        async def _do() -> None:
            assert self._sock

            while self._listen:
                resp = await loop.sock_recv(self._sock, 512)

                if resp.startswith(b"PING"):
                    await loop.sock_sendall(self._sock, b"PONG :tmi.twitch.tv")
                    _log.debug("PING received, sending PONG back")

                if b"JOIN" in resp:
                    _log.info(f"successfully connected to {self.channel}")

                if b"PRIVMSG" not in resp:
                    continue

                data = resp.decode("utf-8").strip()
                _log.debug(f"received message: {data}")
                self.bot.dispatch(
                    kasai.IrcMessageCreateEvent(
                        message=kasai.Message.parse(data), app=self.bot
                    )
                )

        self._task = loop.create_task(_do())

    async def close(self) -> None:
        if self._sock is None:
            raise kasai.NotConnected("no active connections to close")

        if not self._task:
            return

        self._sock.close()
        self._sock = None
        if not self._task.cancelled():
            self._task.cancel()
        self._listen = False
        _log.info(f"successfully closed connection to {self.channel}")

    async def create_message(self, content: str) -> kasai.Message:
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
