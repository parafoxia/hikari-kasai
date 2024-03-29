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
import typing as t
from hashlib import sha256
from time import time

import aiohttp
import irctokens
from hikari.internal import time as time_
from hikari.internal.data_binding import JSONObject
from hikari.internal.ux import TRACE

import kasai
from kasai.errors import NotFound

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
        "_client_id",
        "_client_secret",
        "_api_token",
        "_session",
        "_me",
        "_irc_token",
        "_nickname",
        "_channels",
        "_reader",
        "_writer",
        "_task",
        "_d",
    )

    def __init__(
        self, app: kasai.GatewayBot, irc_token: str, client_id: str, client_secret: str
    ) -> None:
        self._app = app

        self._client_id = client_id
        self._client_secret = client_secret
        self._api_token: str | None = None
        self._session: aiohttp.ClientSession | None = None
        self._me: kasai.User | None = None

        self._irc_token = irc_token
        self._nickname = sha256(f"{time()}".encode("utf-8")).hexdigest()[:7]
        self._channels: list[str] = []
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._task: asyncio.Task[None] | None = None
        self._d = irctokens.stateful.StatefulDecoder()

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
        auth: bool = False,
        options: dict[str, list[str]],
        data: dict[str, t.Any] | None = None,
    ) -> list[JSONObject]:
        def stringify(headers: dict[str, str], body: dict[str, str]) -> str:
            string = "\n".join(
                f"    {k}: {v}"
                if k != "Authorization"
                else f"    {k}: **REDACTED TOKEN**"
                for k, v in headers.items()
            )

            if body:
                copy = body.copy()
                if "client_secret" in copy.keys():
                    copy["client_secret"] = "**REDACTED SECRET**"  # nosec: B105
                if "access_token" in copy.keys():
                    copy["access_token"] = "**REDACTED TOKEN**"  # nosec: B105
                string += f"\n\n    {copy}"

            return string

        if self._session is None:
            raise kasai.NotAlive("there is no active API session")

        if auth:
            url = kasai.TWITCH_TOKEN_URI
            headers = {"Content-Type": "application/json"}
            data = {
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials",
            }
        else:
            query = "?" + "&".join(
                "&".join(f"{key}={v}" for v in value) for key, value in options.items()
            )
            url = kasai.TWITCH_HELIX_URI + route + query
            headers = {
                "Authorization": f"Bearer {self._api_token}",
                "Client-Id": self._client_id,
                "Content-Type": "application/json",
            }
            data = {"data": data} if data else {}

        uuid = time_.uuid()
        trace_enabled = _log.isEnabledFor(TRACE)

        if trace_enabled:
            _log.log(
                TRACE,
                "%s %s %s\n%s",
                uuid,
                method,
                url,
                stringify(headers, data),
            )
            start = time_.monotonic()

        async with self._session.request(
            method, url, headers=headers, json=data
        ) as resp:
            res = await resp.json()

            if not resp.ok:
                raise kasai.RequestFailed(res["status"], res["message"])

        if trace_enabled:
            time_taken = (time_.monotonic() - start) * 1_000
            _log.log(
                TRACE,
                "%s %s %s in %sms\n%s",
                uuid,
                resp.status,
                resp.reason,
                time_taken,
                stringify(dict(resp.headers), res),
            )

        if "data" not in res.keys():
            return [res]
        return t.cast(list[JSONObject], res["data"])

    async def _listen(self) -> None:
        assert self._reader
        assert self._writer
        _log.debug("starting IRC listener...")

        while True:
            payload = await self._reader.read(1_024)
            _log.log(
                TRACE, f"received IRC payload with size {len(payload)}\n    {payload!r}"
            )

            if not payload:
                _log.warning("IRC socket closed unexpectedly, attempting to restart...")
                await self._start_irc()
                break

            lines = self._d.push(payload)
            assert lines

            for line in lines:
                if line.command == "PING":
                    self._writer.write(b"PONG :tmi.twitch.tv\r\n")
                    await self._writer.drain()
                    _log.log(TRACE, "received PING, returned PONG")
                    self.app.dispatch(kasai.PingEvent(app=self.app))
                    continue

                if line.command == "002" and not self._me:
                    self._me = await self.fetch_user(line.params[0])
                    continue

                if line.command == "JOIN":
                    self._channels.append(cn := line.params[0][1:])
                    self.app.dispatch(kasai.JoinEvent(channel=cn, app=self.app))
                    _log.info(f"joined #{cn}")
                    continue

                if line.command == "ROOMSTATE" and line.tags and len(line.tags) > 2:
                    channel = await self.fetch_channel(line.tags["room-id"])
                    self.app.dispatch(kasai.JoinRoomstateEvent(channel=channel))
                    continue

                if line.command == "PART":
                    self._channels.remove(cn := line.params[0][1:])
                    self.app.dispatch(kasai.PartEvent(channel=cn, app=self.app))
                    _log.info(f"parted #{cn}")
                    continue

                if line.command == "CLEARCHAT":
                    event: kasai.ClearEvent | kasai.BanEvent | kasai.TimeoutEvent
                    assert line.tags

                    keys = line.tags.keys()
                    channel = await self.fetch_channel(line.tags["room-id"])
                    created = dt.datetime.fromtimestamp(
                        int(line.tags["tmi-sent-ts"]) / 1000
                    )

                    if "ban-duration" in keys:
                        event = kasai.TimeoutEvent(
                            channel=channel,
                            created_at=created,
                            user=await self.fetch_user(line.tags["target-user-id"]),
                            duration=int(line.tags.get("ban-duration", 0)),
                        )
                    elif "target-user-id" in keys:
                        event = kasai.BanEvent(
                            channel=channel,
                            created_at=created,
                            user=await self.fetch_user(line.tags["target-user-id"]),
                        )
                    else:
                        event = kasai.ClearEvent(channel=channel, created_at=created)

                    self.app.dispatch(event)
                    continue

                if line.command != "PRIVMSG":
                    continue

                assert line.tags
                result = self.app.entity_factory.deserialize_twitch_message(
                    line.params[-1],
                    line.tags,
                    await self._fetch_viewer(line.tags["user-id"], tags=line.tags),
                    await self.fetch_channel(line.tags["room-id"]),
                )
                self.app.dispatch(kasai.MessageCreateEvent(message=result))

    async def _start_api(self) -> None:
        if self.is_alive:
            raise kasai.IsAlive("a client session is already alive")

        self._session = aiohttp.ClientSession()

        res = await self._request("POST", "", auth=True, options={})
        self._api_token = res[0]["access_token"]
        _log.info("api.twitch.tv/helix is ready")

    async def _start_irc(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(
            "irc.chat.twitch.tv", 6667
        )
        _log.debug(f"connected to {self._writer.get_extra_info('peername')}")
        self._writer.write(
            (
                f"PASS {self._irc_token}\r\nNICK {self._nickname}\r\n"
                "CAP REQ :twitch.tv/commands twitch.tv/tags\r\n"
            ).encode(),
        )
        await self._writer.drain()

        def end_task(task: asyncio.Task[None]) -> None:
            try:
                task.result()
            except asyncio.CancelledError:
                ...

        loop = asyncio.get_running_loop()
        self._task = loop.create_task(self._listen())
        self._task.add_done_callback(end_task)
        _log.info("irc.chat.twitch.tv is ready")

    async def start(self) -> None:
        """Start all Twitch services. This is called automatically when
        the Discord bot starts.

        Returns
        -------
        None
        """

        _log.info("starting Twitch services...")

        await self._start_api()
        await self._start_irc()

        _log.info("successfully started all Twitch services!")

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
        assert self._writer

        await self.part(*self._channels)
        await self._session.close()
        self._writer.close()
        await self._writer.wait_closed()

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

        if self._writer is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        if not channels:
            return

        payload = f"JOIN {','.join(f'#{c}' for c in channels)}\r\n".encode()
        self._writer.write(payload)
        await self._writer.drain()

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

        if self._writer is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        if not channels:
            return

        payload = f"PART {','.join(f'#{c}' for c in channels)}\r\n".encode()
        self._writer.write(payload)
        await self._writer.drain()

    async def create_message(
        self, channel: str, content: str, *, reply_to: str | None = None
    ) -> None:
        """Sends a message to a Twitch channel.

        Example
        -------
        ```py
        >>> await bot.twitch.create_message(
            "twitchdev",
            "Never gonna give you up!",
        )
        ```

        Example
        -------
        ```py
        >>> await bot.twitch.create_message(
            "twitchdev",
            "Never gonna let you down!",
            reply_to="885196de-cb67-427a-baa8-82f9b0fcd05f",
        )
        ```

        Parameters
        ----------
        channel : str
            The login username of the channel you want to send a message
            to.
        content : str
            The text content of the message you want to send.

        Other Parameters
        ----------------
        reply_to : str | None
            The Id of the message to reply to. Defaults to `None`.

            .. versionadded:: 0.8a

        Returns
        -------
        None
        """

        if self._writer is None:
            raise kasai.NotAlive("there are no alive IRC websockets")

        channel = channel.strip("#")

        if channel not in self._channels:
            raise kasai.NotJoined("this client has not joined that channel")

        tag = f"@reply-parent-msg-id={reply_to} " if reply_to else ""
        payload = f"{tag}PRIVMSG #{channel} :{content}\r\n".encode("utf-8")

        _log.log(TRACE, f"sending payload with size {len(payload)}\n    {payload!r}")
        self._writer.write(payload)
        await self._writer.drain()

    def get_me(self) -> kasai.User | None:
        """Return the bot user, if known. This should be available
        almost immediately, but may be `None` if the request failed for
        whatever reason.

        Example
        -------
        ```py
        >>> me = bot.twitch.get_me()
        >>> me.id
        141981764
        ```

        Returns
        -------
        kasai.User | None
            The bot user, if available, otherwise `None`.

        .. versionadded:: 0.9a
        """

        return self._me

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
        payload = await self._request("GET", "users", options={key: [user]})

        if not payload:
            raise NotFound(f"no user of ID or login '{user}' exists")

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

        payload = await self._request(
            "GET", "channels", options={"broadcaster_id": [channel]}
        )

        if not payload:
            raise NotFound(f"no channel of '{channel}' exists")

        return self.app.entity_factory.deserialize_twitch_channel(payload[0])

    async def _fetch_viewer(self, user: str, *, tags: dict[str, str]) -> kasai.Viewer:
        key = "id" if user.isdigit() else "login"
        payload = await self._request("GET", "users", options={key: [user]})

        if not payload:
            raise NotFound(f"no user by ID or login '{user}' exists")

        return self.app.entity_factory.deserialize_twitch_viewer(payload[0], tags)

    async def fetch_stream(self, user: str) -> kasai.Stream:
        """Fetches a stream from the Twitch Helix API.

        Example
        -------
        ```py
        >>> stream1 = await bot.twitch.fetch_stream("twitchdev")
        >>> stream2 = await bot.twitch.fetch_stream("141981764")
        >>> stream1 == stream2
        True
        ```

        Parameters
        ----------
        user : str
            The login username or the ID of the user whose stream you
            want to fetch. Note that while Twitch user IDs are
            numerical, they are strings.

        Returns
        -------
        kasai.Stream
            The fetched stream.

        .. versionadded:: 0.10a
        """

        key = "user_id" if user.isdigit() else "user_login"
        payload = await self._request("GET", "streams", options={key: [user]})

        if not payload:
            raise NotFound(f"no stream by a channel of ID or login '{user}' exists")

        return self.app.entity_factory.deserialize_twitch_stream(payload[0])
