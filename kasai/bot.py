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

__all__ = ("GatewayBot",)

import logging
import typing as t
from importlib.util import find_spec

import hikari

import kasai
from kasai import entity_factory, traits

_log = logging.getLogger(__name__)


class GatewayBot(hikari.GatewayBot, traits.TwitchAware):
    """A class representing a Discord bot. This extends
    `hikari.GatewayBot`.

    To extend command handler classes, you should create a subclass that
    inherits from this class and your preferred command handler's bot
    class (making sure you inherit from this class first).

    Example:

    ```py
    class MyBot(kasai.GatewayBot, lightbulb.BotApp):
        ...

    bot = MyBot(...)
    ```

    Parameters
    ----------
    token : str
        Your Discord bot's token.
    irc_token : str
        Your Twitch IRC access token. This is different to an API access
        token.
    client_id : str
        Your Twitch application's client ID.
    client_secret : str
        Your Twitch application's client secret.

    Other Parameters
    ----------------
    banner : str
        The banner to be displayed on boot (this is passed directly to
        the superclass initialiser). This defaults to "kasai".
    **kwargs : Any
        Additional keyword arguments to be passed to the superclasses.
    """

    def __init__(
        self,
        token: str,
        irc_token: str,
        client_id: str,
        client_secret: str,
        *,
        banner: str = "kasai",
        **kwargs: t.Any,
    ) -> None:
        super().__init__(token, banner=banner, **kwargs)
        self._entity_factory: entity_factory.TwitchEntityFactoryImpl

        self._entity_factory = entity_factory.TwitchEntityFactoryImpl(self)
        self._twitch = kasai.TwitchClient(self, irc_token, client_id, client_secret)

    @property
    def entity_factory(self) -> entity_factory.TwitchEntityFactory:
        """This client's entity factory.

        Returns
        -------
        kasai.entity_factory.TwitchEntityFactory
        """

        return self._entity_factory

    @property
    def twitch(self) -> kasai.TwitchClient:
        """The Twitch client.

        Returns
        -------
        kasai.twitch.TwitchClient
        """

        return self._twitch

    async def start(self, **kwargs: t.Any) -> None:
        """Starts the Twitch and Discord clients (in that order). This
        often does not need to be called, as `kasai.GatewayBot.run` will
        call this automatically.

        Other Parameters
        ----------------
        **kwargs : Any
            Additional arguments to be passed to
            `hikari.GatewayBot.start`.
        """

        await self._twitch.start()
        await super().start(**kwargs)

    async def _close(self) -> None:
        if self._twitch.is_alive:
            await self._twitch.close()

        await super()._close()

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
