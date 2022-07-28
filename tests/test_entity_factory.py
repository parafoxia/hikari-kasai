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

import datetime as dt
import typing as t

import pytest
from dateutil.tz import tzutc

import kasai
from kasai.entity_factory import TwitchEntityFactoryImpl
from kasai.users import BroadcasterType, UserType


@pytest.fixture()
def entity_factory() -> TwitchEntityFactoryImpl:
    app = kasai.GatewayBot("token", "irc_token", "client_id", "client_secret")
    return TwitchEntityFactoryImpl(app)


@pytest.fixture()
def user_payload() -> dict[str, t.Any]:
    return {
        "id": "141981764",
        "login": "twitchdev",
        "display_name": "TwitchDev",
        "type": "",
        "broadcaster_type": "partner",
        "description": "Supporting third-party developers building Twitch integrations from chatbots to game integrations.",
        "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png",
        "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png",
        "view_count": 5980557,
        "email": "not-real@email.com",
        "created_at": "2016-12-14T20:32:28Z",
    }


def test_deserialise_user(
    entity_factory: TwitchEntityFactoryImpl, user_payload: dict[str, t.Any]
) -> None:
    user = entity_factory.deserialize_twitch_user(user_payload)
    assert isinstance(user, kasai.User)

    assert isinstance(user.app, kasai.GatewayBot)
    assert user.broadcaster_type == BroadcasterType.PARTNER
    assert (
        user.description
        == "Supporting third-party developers building Twitch integrations from chatbots to game integrations."
    )
    assert user.display_name == "TwitchDev"
    assert user.id == "141981764"
    assert user.username == "twitchdev"
    assert (
        user.offline_image_url
        == "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png"
    )
    assert (
        user.profile_image_url
        == "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png"
    )
    assert user.type == UserType.NORMAL
    assert user.created_at == dt.datetime(2016, 12, 14, 20, 32, 28, tzinfo=tzutc())


@pytest.fixture()
def tags() -> dict[str, str]:
    return {
        "badge-info": "",
        "badges": "broadcaster/1",
        "client-nonce": "459e3142897c7a22b7d275178f2259e0",
        "color": "#0000FF",
        "display-name": "lovingt3s",
        "emote-only": "1",
        "emotes": "62835:0-10",
        "first-msg": "0",
        "flags": "",
        "id": "885196de-cb67-427a-baa8-82f9b0fcd05f",
        "mod": "0",
        "room-id": "713936733",
        "subscriber": "0",
        "tmi-sent-ts": "1643904084794",
        "turbo": "0",
        "user-id": "713936733",
        "user-type": "",
    }


def test_deserialise_viewer(
    entity_factory: TwitchEntityFactoryImpl,
    user_payload: dict[str, t.Any],
    tags: dict[str, str],
) -> None:
    viewer = entity_factory.deserialize_twitch_viewer(user_payload, tags)
    assert isinstance(viewer, kasai.Viewer)

    assert isinstance(viewer.app, kasai.GatewayBot)
    assert viewer.broadcaster_type == BroadcasterType.PARTNER
    assert (
        viewer.description
        == "Supporting third-party developers building Twitch integrations from chatbots to game integrations."
    )
    assert viewer.display_name == "TwitchDev"
    assert viewer.id == "141981764"
    assert viewer.username == "twitchdev"
    assert (
        viewer.offline_image_url
        == "https://static-cdn.jtvnw.net/jtv_user_pictures/3f13ab61-ec78-4fe6-8481-8682cb3b0ac2-channel_offline_image-1920x1080.png"
    )
    assert (
        viewer.profile_image_url
        == "https://static-cdn.jtvnw.net/jtv_user_pictures/8a6381c7-d0c0-4576-b179-38bd5ce1d6af-profile_image-300x300.png"
    )
    assert viewer.type == UserType.NORMAL
    assert viewer.created_at == dt.datetime(2016, 12, 14, 20, 32, 28, tzinfo=tzutc())

    assert viewer.color == 255
    assert viewer.colour == viewer.color
    assert viewer.is_mod == False
    assert viewer.is_subscriber == False
    assert viewer.is_turbo == False
    assert viewer.is_broadcaster == True


@pytest.fixture()
def channel_payload() -> dict[str, t.Any]:
    return {
        "broadcaster_id": "141981764",
        "broadcaster_login": "twitchdev",
        "broadcaster_name": "TwitchDev",
        "broadcaster_language": "en",
        "game_id": "509670",
        "game_name": "Science & Technology",
        "title": "TwitchDev Monthly Update // May 6, 2021",
        "delay": 0,
    }


def test_deserialise_channel(
    entity_factory: TwitchEntityFactoryImpl, channel_payload: dict[str, t.Any]
) -> None:
    game = kasai.Game(name="Science & Technology", id="509670")

    channel = entity_factory.deserialize_twitch_channel(channel_payload)
    assert isinstance(channel, kasai.Channel)

    assert isinstance(channel.app, kasai.GatewayBot)
    assert channel.id == "141981764"
    assert channel.username == "twitchdev"
    assert channel.display_name == "TwitchDev"
    assert channel.language == "en"
    assert channel.game == game
    assert channel.title == "TwitchDev Monthly Update // May 6, 2021"
    assert channel.delay == 0


@pytest.fixture()
def message_payload() -> str:
    return "PRIVMSG #twitchdev :HeyGuys <3 PartyTime"


def test_deserialise_message(
    entity_factory: TwitchEntityFactoryImpl,
    user_payload: dict[str, t.Any],
    tags: dict[str, str],
    channel_payload: dict[str, t.Any],
    message_payload: str,
) -> None:
    message = entity_factory.deserialize_twitch_message(
        message_payload,
        tags,
        viewer := entity_factory.deserialize_twitch_viewer(user_payload, tags),
        channel := entity_factory.deserialize_twitch_channel(channel_payload),
    )
    assert isinstance(message, kasai.Message)

    assert isinstance(message.app, kasai.GatewayBot)
    assert message.id == "885196de-cb67-427a-baa8-82f9b0fcd05f"
    assert message.author == viewer
    assert message.channel == channel
    assert message.created_at == dt.datetime(2022, 2, 3, 16, 1, 24, 794000)
    assert message.bits == 0
    assert message.content == "HeyGuys <3 PartyTime"
