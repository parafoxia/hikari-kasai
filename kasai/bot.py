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

import asyncio

__all__ = ("GatewayApp", "LightbulbApp", "CrescentApp")

import logging
import typing as t

import hikari
from pkg_resources import working_set

import kasai

_libs = [p.key for p in working_set]

_log = logging.getLogger(__name__)


class GatewayApp(hikari.GatewayBot):
    # __slots__ = ("_irc",)

    def __init__(
        self,
        token: str,
        irc_token: str,
        irc_channel: str,
        irc_nickname: str,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(token, **kwargs)
        self._irc = kasai.IrcClient(self, irc_token, irc_channel, irc_nickname)

    @property
    def irc(self) -> kasai.IrcClient:
        return self._irc

    async def start_irc(self) -> None:
        if self._irc._sock is not None:
            raise kasai.AlreadyConnected("there is already an active connection")

        loop = asyncio.get_running_loop()
        self._irc._create_sock()
        assert self._irc._sock is not None

        await loop.sock_connect(self._irc._sock, ("irc.chat.twitch.tv", 6667))
        await loop.sock_sendall(
            self._irc._sock,
            (
                f"PASS {self._irc._token}\r\n"
                f"NICK {self._irc.nickname}\r\n"
                f"JOIN {self._irc.channel}\r\n"
            ).encode("utf-8"),
        )

        self._irc._task = loop.create_task(self._irc._listen(loop))
        _log.info("successfully started IRC websocket")

    async def close_irc(self) -> None:
        if self._irc._sock is None:
            raise kasai.NotConnected("no active connections to close")

        if not self._irc._task:
            return

        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self._irc._sock, b"PART\r\n")
        self._irc._sock.close()
        self._irc._sock = None
        if not self._irc._task.cancelled():
            self._irc._task.cancel()
        _log.info("successfully closed IRC websocket")

    async def _close(self) -> None:
        if self._irc.is_alive:
            await self.close_irc()
        return await super()._close()

    @staticmethod
    def print_banner(
        banner: str | None,
        allow_color: bool,
        force_color: bool,
        extra_args: dict[str, str] | None = None,
    ) -> None:
        super(GatewayApp, GatewayApp).print_banner(
            banner, allow_color, force_color, extra_args
        )
        print(
            f"Thanks for using "
            f"\33[1m\33[38;5;1m火\33[38;5;208m災 \33[38;5;3mkasai\33[0m "
            f"(v\33[1m{kasai.__version__}\33[0m)!\n"
        )


if "hikari-lightbulb" in _libs:
    import lightbulb

    class LightbulbApp(GatewayApp, lightbulb.BotApp):
        ...


if "hikari-crescent" in _libs:
    import crescent

    class CrescentApp(GatewayApp, crescent.Bot):
        ...
