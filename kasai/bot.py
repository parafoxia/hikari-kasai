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
from importlib.util import find_spec

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
    bot class. Note that if you do this, Kasai's GatewayBot *must* be
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
        banner:
            The banner to be displayed on boot (this is passed directly
            to the :obj:`~hikari.impl.bot.GatewayBot` initialiser). This
            defaults to "kasai".
        **kwargs:
            Additional keyword arguments to be passed to
            :obj:`~hikari.impl.bot.GatewayBot`.

    .. versionchanged:: 0.6a
        (1) This no longer takes ``channel`` and ``nickname`` arguments.
        (2) You can now choose the banner that will be displayed on
        boot.
    """

    def __init__(
        self,
        token: str,
        irc_token: str,
        *,
        banner: str = "kasai",
        **kwargs: t.Any,
    ) -> None:
        super().__init__(token, banner=banner, **kwargs)
        self._twitch = kasai.TwitchClient(self, irc_token)

    @property
    def twitch(self) -> kasai.TwitchClient:
        """The Twitch IRC client interface.

        Returns:
            :obj:`kasai.twitch.TwitchClient`

        .. versionadded:: 0.4a
        """

        return self._twitch

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

        .. versionchanged:: 0.4a
            This now takes channels as an argument.
        """

        if self._twitch._sock is not None:
            raise kasai.AlreadyConnected("there is already an active connection")

        loop = asyncio.get_running_loop()
        self._twitch._create_sock()
        assert self._twitch._sock is not None

        await loop.sock_connect(self._twitch._sock, ("irc.chat.twitch.tv", 6667))
        _log.info("connected to Twitch")

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

        await self._twitch.part(*self._twitch._channels)
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
