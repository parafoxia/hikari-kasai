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
import datetime as dt
import logging
import socket
import typing as t
from hashlib import sha256
from time import time

import aiohttp
from hikari.internal.data_binding import JSONObject

import kasai

_log = logging.getLogger(__name__)


class TwitchClient:
    """A class representing a Twitch client.

    Parameters
    ----------
    app : kasai.GatewayBot
        The base client application.
    irc_token : str
        Your Twitch IRC access token. This is different to an API access
        token.
    client_id : str
        Your Twitch application's client ID.
    client_secret : str
        Your Twitch application's client secret.
    """

    __slots__ = (
        "_app",
        "_irc_token",
        "_client_id",
        "_client_secret",
        "_api_token",
        "_session",
        "_nickname",
        "_channels",
        "_sock",
        "_task",
    )

    def __init__(
        self, app: kasai.GatewayBot, irc_token: str, client_id: str, client_secret: str
    ) -> None:
        self._app = app

        self._irc_token = irc_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_token: str | None = None
        self._session: aiohttp.ClientSession | None = None

        self._nickname = sha256(f"{time()}".encode("utf-8")).hexdigest()[:7]
        self._channels: list[str] = []
        self._sock: socket.socket | None = None
        self._task: asyncio.Task[None] | None = None

    @property
    def is_alive(self) -> bool:
        """Whether the client is connected to the Twitch Helix API. This
        does not necessarily mean the client is connected to the Twitch
        IRC servers."""

        return self._session is not None and not self._session.closed

    @property
    def is_authorised(self) -> bool:
        """Whether the client is authorised to connect to the Twitch
        Helix API."""

        return self._api_token is not None

    @property
    def app(self) -> kasai.GatewayBot:
        """The base client application."""

        return self._app

    @staticmethod
    def _transform_tags(tags: str) -> dict[str, str]:
        return {(kv := tag.split("="))[0]: kv[1] for tag in tags[1:].split(";")}

    async def _request(
        self,
        method: str,
        route: str,
        *,
        options: dict[str, list[str]],
    ) -> list[JSONObject]:
        if self._session is None:
            raise kasai.NotAlive("there is no active API session")

        query = "?"
        for key, value in options.items():
            query += "&".join(f"{key}={v}" for v in value)

        async with self._session.request(
            method,
            kasai.TWITCH_HELIX_URI + route + query,
            headers={
                "Authorization": f"Bearer {self._api_token}",
                "Client-Id": self._client_id,
            },
        ) as resp:
            data = await resp.json()

            if not resp.ok:
                raise kasai.RequestFailed(data["status"], data["message"])

        return t.cast(list[JSONObject], data["data"])

    async def _listen(self) -> None:
        assert self._sock
        loop = asyncio.get_running_loop()

        while True:
            payload = (await loop.sock_recv(self._sock, 512)).decode("utf-8").strip()
            _log.debug(f"received IRC message: {payload}")

            for data in payload.split("\n"):
                if data.startswith("@"):
                    raw_tags, message = data.split(" ", maxsplit=1)
                    tags = self._transform_tags(raw_tags)
                else:
                    message = data
                    tags = {}

                if message.startswith("PING"):
                    await loop.sock_sendall(self._sock, b"PONG :tmi.twitch.tv\r\n")
                    self.app.dispatch(kasai.PingEvent(app=self.app))
                    continue

                if "JOIN" in message:
                    self._channels.append(cn := message.split()[-1][1:])
                    self.app.dispatch(kasai.JoinEvent(channel=cn, app=self.app))
                    _log.info(f"joined #{cn}")
                    continue

                if "ROOMSTATE" in message and len(tags) > 2:
                    channel = await self.fetch_channel(tags["room-id"])
                    self.app.dispatch(kasai.JoinRoomstateEvent(channel=channel))
                    continue

                if "PART" in message:
                    self._channels.remove(cn := message.split()[-1][1:])
                    self.app.dispatch(kasai.PartEvent(channel=cn, app=self.app))
                    _log.info(f"parted #{cn}")
                    continue

                if "CLEARCHAT" in message:
                    event: kasai.ClearEvent | kasai.BanEvent | kasai.TimeoutEvent
                    keys = tags.keys()

                    channel = await self.fetch_channel(tags["room-id"])
                    created = dt.datetime.fromtimestamp(int(tags["tmi-sent-ts"]) / 1000)

                    if "ban-duration" in keys:
                        event = kasai.TimeoutEvent(
                            channel=channel,
                            created_at=created,
                            user=await self.fetch_user(tags["target-user-id"]),
                            duration=int(tags.get("ban-duration", 0)),
                        )
                    elif "target-user-id" in keys:
                        event = kasai.BanEvent(
                            channel=channel,
                            created_at=created,
                            user=await self.fetch_user(tags["target-user-id"]),
                        )
                    else:
                        event = kasai.ClearEvent(channel=channel, created_at=created)

                    self.app.dispatch(event)
                    continue

                if "PRIVMSG" not in message:
                    continue

                user = message[(i := message.index("#") + 1) : message.index(" ", i)]
                result = self.app.entity_factory.deserialize_twitch_message(
                    message,
                    tags,
                    await self._fetch_viewer(user, tags=tags),
                    await self.fetch_channel(tags["room-id"]),
                )
                self.app.dispatch(kasai.MessageCreateEvent(message=result))

    async def start(self) -> None:
        """Start all Twitch services. This is called automatically when
        the Discord bot starts.

        Returns
        -------
        None
        """

        if self.is_alive:
            raise kasai.IsAlive("a client session is already alive")

        # Enable API requests.
        self._session = aiohttp.ClientSession()

        async with self._session.post(
            kasai.TWITCH_TOKEN_URI,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials",
            },
        ) as resp:
            data = await resp.json()
            self._api_token = data["access_token"]

        # Open an IRC websocket.
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setblocking(False)

        loop = asyncio.get_running_loop()
        await loop.sock_connect(self._sock, ("irc.chat.twitch.tv", 6667))
        await loop.sock_sendall(
            self._sock,
            (
                f"PASS {self._irc_token}\r\nNICK {self._nickname}\r\n"
                "CAP REQ :twitch.tv/commands twitch.tv/tags\r\n"
            ).encode(),
        )

        self._task = loop.create_task(self._listen())
        self._task.add_done_callback(lambda task: task.result())

        # Finish up.
        _log.info("successfully started Twitch services")

    async def close(self) -> None:
        """Ends all Twitch services. This is called automatically when
        the Discord bot shuts down.

        Returns
        -------
        None
        """

        if not self.is_alive:
            raise kasai.NotAlive(
                "Twitch services were never started, or have already been shut down"
            )

        assert self._session
        assert self._sock

        await self.part(*self._channels)
        await self._session.close()
        self._sock.close()
        self._sock = None

        if self._task and not self._task.cancelled():
            self._task.cancel()

        _log.info("successfully closed IRC websocket")

    async def join(self, *channels: str) -> None:
        """Joins the given Twitch channels' chats.

        Example
        -------
        ```py
        >>> await bot.twitch.join("twitch", "twitchdev")
        ```

        Example
        -------
        ```py
        >>> channels = ("twitch", "twitchdev")
        >>> await bot.twitch.join(*channels)
        ```

        Parameters
        ----------
        *channels : str
            The login usernames of the channels to join.

        Returns
        -------
        None
        """

        if self._sock is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        if not channels:
            return

        loop = asyncio.get_running_loop()
        msg = "\r\n".join(f"JOIN #{c}" for c in channels) + "\r\n"
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))

    async def part(self, *channels: str) -> None:
        """Parts (leaves) the given Twitch channels' chats.

        .. note::
            You do not need to part joined channels before shutting the
            bot down — this is handled automatically.

        Example
        -------
        ```py
        >>> await bot.twitch.part("twitch", "twitchdev")
        ```

        Example
        -------
        ```py
        >>> channels = ("twitch", "twitchdev")
        >>> await bot.twitch.part(*channels)
        ```

        Parameters
        ----------
        *channels : str
            The login usernames of the channels to part.

        Returns
        -------
        None
        """

        if self._sock is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        if not channels:
            return

        loop = asyncio.get_running_loop()
        msg = "\r\n".join(f"PART #{c}" for c in channels) + "\r\n"
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))

    async def create_message(self, channel: str, content: str) -> None:
        """Send a message to a Twitch channel.

        Example
        -------
        ```py
        >>> await bot.twitch.create_message(
            "twitchdev",
            "Never gonna give you up!",
        )
        ```

        Parameters
        ----------
        channel : str
            The login username of the channel you want to send a message
            to.
        content : str
            The text content of the message you want to send.

        Returns
        -------
        None
        """

        if self._sock is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        channel = channel.strip("#")

        if channel not in self._channels:
            raise kasai.NotJoined("this client has not joined that channel")

        msg = (
            f":{self._nickname}!{self._nickname}@{self._nickname}.tmi.twitch.tv "
            f"PRIVMSG #{channel} :{content}\r\n"
        )
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self._sock, msg.encode("utf-8"))

    async def fetch_user(self, user: str) -> kasai.User:
        """Fetches a user from the Twitch Helix API.

        Example
        -------
        ```py
        >>> user1 = await bot.twitch.fetch_user("twitchdev")
        >>> user2 = await bot.twitch.fetch_user("141981764")
        >>> user1 == user2
        True
        ```

        Parameters
        ----------
        user : str
            The login username or the ID of the user to fetch. Note that
            while Twitch user IDs are numerical, they are strings.

        Returns
        -------
        kasai.User
            The fetched user.
        """

        key = "id" if user.isdigit() else "login"
        payload = await self.app.twitch._request("GET", "users", options={key: [user]})
        return self.app.entity_factory.deserialize_twitch_user(payload[0])

    async def fetch_channel(self, channel: str) -> kasai.Channel:
        """Fetches a channel from the Twitch Helix API.

        Example
        -------
        ```py
        >>> channel = await bot.twitch.fetch_channel("141981764")
        >>> print(channel.username)
        twitchdev
        ```

        Parameters
        ----------
        channel : str
            The ID of the channel to fetch. Note that while Twitch
            channel IDs are numerical, they are strings. A channel's ID
            is identical to the user ID of the channel.

        Returns
        -------
        kasai.Channel
            The fetched channel.
        """

        payload = await self.app.twitch._request(
            "GET", "channels", options={"broadcaster_id": [channel]}
        )
        return self.app.entity_factory.deserialize_twitch_channel(payload[0])

    async def _fetch_viewer(self, user: str, *, tags: dict[str, str]) -> kasai.Viewer:
        key = "id" if user.isdigit() else "login"
        payload = await self.app.twitch._request("GET", "users", options={key: [user]})
        return self.app.entity_factory.deserialize_twitch_viewer(payload[0], tags)
