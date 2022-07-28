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

import re

import pytest

import kasai

_NICK_PATTERN = re.compile(r"[a-f0-9]{7}")


@pytest.fixture()
def client() -> kasai.TwitchClient:
    app = kasai.GatewayBot("token", "irc_token", "client_id", "client_secret")
    return kasai.TwitchClient(app, "irc_token", "client_id", "client_secret")


def test_initial_attributes(client: kasai.TwitchClient) -> None:
    assert client._irc_token == "irc_token"
    assert client._client_id == "client_id"
    assert client._client_secret == "client_secret"
    assert client._api_token is None
    assert client._session is None
    assert _NICK_PATTERN.match(client._nickname)
    assert client._channels == []
    assert client._sock is None
    assert client._task is None


def test_initial_is_alive_property(client: kasai.TwitchClient) -> None:
    assert not client.is_alive


def test_initial_is_authorised_property(client: kasai.TwitchClient) -> None:
    assert not client.is_authorised


def test_app_property(client: kasai.TwitchClient) -> None:
    assert isinstance(client.app, kasai.GatewayBot)
    assert client.app == client._app


def test_transform_tags(client: kasai.TwitchClient) -> None:
    raw = "@room-id=12345678;target-user-id=87654321;tmi-sent-ts=1642715756806"
    assert client._transform_tags(raw) == {
        "room-id": "12345678",
        "target-user-id": "87654321",
        "tmi-sent-ts": "1642715756806",
    }
