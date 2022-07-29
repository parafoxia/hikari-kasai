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

__all__ = ("TwitchEntityFactory", "TwitchEntityFactoryImpl")

import abc
import datetime as dt
import typing as t

from dateutil.parser import parse as parse_dt
from hikari.api import EntityFactory
from hikari.impl import EntityFactoryImpl
from hikari.internal import data_binding

from kasai import channels, games, messages, traits, users


class TwitchEntityFactory(EntityFactory, abc.ABC):
    __slots__: t.Sequence[str] = ()

    @abc.abstractmethod
    def deserialize_twitch_user(self, payload: data_binding.JSONObject) -> users.User:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize_twitch_viewer(
        self, payload: data_binding.JSONObject, tags: dict[str, str]
    ) -> users.Viewer:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize_twitch_channel(
        self, payload: data_binding.JSONObject
    ) -> channels.Channel:
        raise NotImplementedError

    @abc.abstractmethod
    def deserialize_twitch_message(
        self,
        message: str,
        tags: dict[str, str],
        viewer: users.Viewer,
        channel: channels.Channel,
    ) -> messages.Message:
        raise NotImplementedError


class TwitchEntityFactoryImpl(EntityFactoryImpl, TwitchEntityFactory):
    __slots__: t.Sequence[str] = ()

    def __init__(self, app: traits.TwitchAware):
        self._app: traits.TwitchAware
        super().__init__(app)

    def deserialize_twitch_user(self, payload: data_binding.JSONObject) -> users.User:
        return users.UserImpl(
            app=self._app,
            broadcaster_type=users.BroadcasterType(payload["broadcaster_type"]),
            description=payload["description"],
            display_name=payload["display_name"],
            id=payload["id"],
            username=payload["login"],
            offline_image_url=payload["offline_image_url"],
            profile_image_url=payload["profile_image_url"],
            type=users.UserType(payload["type"]),
            created_at=parse_dt(payload["created_at"]),
        )

    def deserialize_twitch_viewer(
        self, payload: data_binding.JSONObject, tags: dict[str, str]
    ) -> users.Viewer:
        return users.ViewerImpl(
            app=self._app,
            broadcaster_type=users.BroadcasterType(payload["broadcaster_type"]),
            description=payload["description"],
            display_name=payload["display_name"],
            id=payload["id"],
            username=payload["login"],
            offline_image_url=payload["offline_image_url"],
            profile_image_url=payload["profile_image_url"],
            type=users.UserType(payload["type"]),
            created_at=parse_dt(payload["created_at"]),
            color=int(tags.get("color", "#0")[1:], base=16),
            is_mod=bool(int(tags["mod"])),
            is_subscriber=bool(int(tags["subscriber"])),
            is_turbo=bool(int(tags["turbo"])),
            is_broadcaster="broadcaster" in tags["badges"],
        )

    def deserialize_twitch_channel(
        self, payload: data_binding.JSONObject
    ) -> channels.Channel:
        return channels.Channel(
            app=self._app,
            id=payload["broadcaster_id"],
            username=payload["broadcaster_login"],
            display_name=payload["broadcaster_name"],
            language=payload["broadcaster_language"],
            game=games.Game(id=payload["game_id"], name=payload["game_name"]),
            title=payload["title"],
            delay=payload["delay"],
        )

    def deserialize_twitch_message(
        self,
        message: str,
        tags: dict[str, str],
        viewer: users.Viewer,
        channel: channels.Channel,
    ) -> messages.Message:
        return messages.Message(
            app=self._app,
            id=tags["id"],
            author=viewer,
            channel=channel,
            created_at=dt.datetime.fromtimestamp(int(tags["tmi-sent-ts"]) / 1000),
            bits=int(tags.get("bits", 0)),
            content=message.split(":")[-1],
        )
