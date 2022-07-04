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

__all__ = ("GatewayBot", "GatewayApp", "LightbulbApp", "CrescentApp")

import asyncio
import logging
import typing as t
from hashlib import sha256
from importlib.util import find_spec
from time import time

import hikari
from pkg_resources import working_set

import kasai
from kasai import ux

_libs = [p.key for p in working_set]

_log = logging.getLogger(__name__)


class GatewayBot(hikari.GatewayBot):
    """A subclass of :obj:`~hikari.impl.bot.GatewayBot` which includes
    Twitch functionality.

    If you wish to use a command handler, you can create a subclass
    which inherits from this class and your preferred command handler's
    bot class. Note that if you do this, Kasai's GatewayApp *must* be
    inherited first.

    For example:

    .. code-block:: python

        class Bot(kasai.GatewayBot, lightbulb.BotApp):
            ...

        bot = Bot(...)

    Args:
        token:
            Your Discord bot's token.
        irc_token:
            Your Twitch IRC access token.

    Keyword Args:
        **kwargs:
            Additional keyword arguments to be passed to
            :obj:`~hikari.impl.bot.GatewayBot`.
    """

    def __init__(
        self,
        token: str,
        irc_token: str,
        channel: str | None = None,
        nickname: str | None = None,
        /,
        **kwargs: t.Any,
    ) -> None:
        if channel:
            ux.depr_warn(
                "channel",
                "v0.6a",
                (
                    "the 'channel' argument should now be passed to "
                    "GatewayBot.start_irc — it no longer works here"
                ),
            )

        if nickname:
            ux.depr_warn(
                "nickname", "v0.6a", "the 'nickname' argument is no longer in use"
            )

        super().__init__(token, banner="kasai", **kwargs)
        self._twitch = kasai.TwitchClient(self, irc_token)

    @property
    def irc(self) -> kasai.TwitchClient:
        ux.depr_warn(
            "GatewayBot.irc",
            "0.6a",
            (
                "use `GatewayBot.twitch` instead. The old IRC client has been replaced "
                "with a new Twitch one, which means that there are some breaking "
                "changes that could not be deprecated"
            ),
        )
        return self._twitch

    @property
    def twitch(self) -> kasai.TwitchClient:
        """The Twitch IRC client interface.

        Returns:
            :obj:`kasai.twitch.TwitchClient`
        """

        return self._twitch

    @staticmethod
    def _unique_id() -> str:
        return sha256(f"{time()}".encode("utf-8")).hexdigest()[:7]

    async def start_irc(self, *channels: str) -> None:
        """Create a websocket connection to Twitch's IRC servers and
        start listening for messages.

        Args:
            *channels:
                The channels to join once connected. This can be empty,
                in which case you will need to manually join your
                channel(s) later. All channels must be prefixed with a
                hash (#).

        Raises:
            :obj:`kasai.errors.AlreadyConnected`:
                Kasai is already connected to a Twitch channel.
        """

        if self._twitch._sock is not None:
            raise kasai.AlreadyConnected("there is already an active connection")

        loop = asyncio.get_running_loop()
        self._twitch._create_sock()
        assert self._twitch._sock is not None

        await loop.sock_connect(self._twitch._sock, ("irc.chat.twitch.tv", 6667))
        _log.info("connected to Twitch")

        self._twitch._nickname = self._unique_id()
        await loop.sock_sendall(
            self._twitch._sock,
            (
                f"PASS {self._twitch._token}\r\n"
                f"NICK {self._twitch._nickname}\r\n"
                "CAP REQ :twitch.tv/commands twitch.tv/tags\r\n"
            ).encode(),
        )

        self._twitch._task = loop.create_task(self._twitch._irclisten(loop))
        _log.info("successfully started IRC websocket")

        if channels:
            await self._twitch.join(*channels)

    async def close_irc(self) -> None:
        """Stop listening for messages and close the connection to your
        Twitch channel(s).

        Raises:
            :obj:`kasai.errors.NotConnected`:
                Kasai is not currently connected to a Twitch channel.
        """

        if self._twitch._sock is None:
            raise kasai.NotConnected("no active connections to close")

        if not self._twitch._task:
            return

        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self._twitch._sock, b"PART\r\n")
        self._twitch._sock.close()
        self._twitch._sock = None
        if not self._twitch._task.cancelled():
            self._twitch._task.cancel()
        _log.info("successfully closed IRC websocket")

    async def _close(self) -> None:
        if self._twitch.is_alive:
            await self.close_irc()
        return await super()._close()

    @staticmethod
    def print_banner(
        banner: str | None,
        allow_color: bool,
        force_color: bool,
        extra_args: dict[str, str] | None = None,
    ) -> None:
        def _install_location() -> str:
            spec = find_spec("kasai")

            if spec:
                if spec.submodule_search_locations:
                    return spec.submodule_search_locations[0]

            return "unknown"

        args = {
            "kasai_icon": "\33[1m\33[38;5;1m火\33[38;5;208m災",
            "hikari_icon": "\33[1m\33[38;5;135m光",
            "kasai_version": kasai.__version__,
            "kasai_install_location": _install_location(),
            "kasai_documentation_url": kasai.__docs__,
            "c1": "\33[1m\33[38;5;196m",
            "c2": "\33[1m\33[38;5;202m",
            "c3": "\33[1m\33[38;5;166m",
            "c4": "\33[1m\33[38;5;172m",
            "c5": "\33[1m\33[38;5;214m",
            "c6": "\33[1m\33[38;5;227m",
            "c7": "\33[1m\33[38;5;229m",
            "c8": "\33[1m\33[38;5;231m",
        }

        if extra_args:
            args.update(extra_args)

        super(GatewayBot, GatewayBot).print_banner(
            banner, allow_color, force_color, extra_args=args
        )


class GatewayApp(GatewayBot):
    def __init__(
        self,
        token: str,
        irc_token: str,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(token, irc_token, **kwargs)
        ux.depr_warn("kasai.GatewayApp", "0.7a", "use 'kasai.GatewayBot' instead")


if "hikari-lightbulb" in _libs:
    import lightbulb

    class LightbulbApp(GatewayBot, lightbulb.BotApp):
        def __init__(
            self,
            token: str,
            irc_token: str,
            **kwargs: t.Any,
        ) -> None:
            super().__init__(token, irc_token, **kwargs)
            ux.depr_warn(
                "kasai.LightbulbApp",
                "0.7a",
                (
                    "you will need to subclass to use command handlers in future; "
                    "refer to README for more information"
                ),
            )


if "hikari-crescent" in _libs:
    import crescent

    class CrescentApp(GatewayBot, crescent.Bot):
        def __init__(
            self,
            token: str,
            irc_token: str,
            **kwargs: t.Any,
        ) -> None:
            super().__init__(token, irc_token, **kwargs)
            ux.depr_warn(
                "kasai.CrescentApp",
                "0.7a",
                (
                    "you will need to subclass to use command handlers in future; "
                    "refer to README for more information"
                ),
            )
