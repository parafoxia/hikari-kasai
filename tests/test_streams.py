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

import pytest
from dateutil.tz import tzutc

import kasai


@pytest.fixture()
def stream() -> kasai.Stream:
    app = kasai.GatewayBot("token", "irc_token", "client_id", "client_secret")
    return kasai.Stream(
        app=app,
        id="40944942733",
        channel=kasai.Channel(
            app=app,
            id="67931625",
            username="amar",
            display_name="Amar",
            language="de",
            game=kasai.Game(
                id="33214",
                name="Fortnite",
            ),
            title="27h Stream Pringles Deathrun Map + 12k MK Turnier | !sub !JustLegends !Pc !yfood",
            delay=None,
        ),
        type=kasai.StreamType.LIVE,
        viewer_count=14944,
        # Custom time to make tests easier.
        created_at=dt.datetime.now(tz=tzutc()) - dt.timedelta(seconds=3600),
        is_mature=False,
        thumbnail_url="https://static-cdn.jtvnw.net/previews-ttv/live_user_amar-{width}x{height}.jpg",
    )


def test_uptime_property(stream: kasai.Stream) -> None:
    # Need to give it an operating window.
    assert dt.timedelta(seconds=3600) < stream.uptime < dt.timedelta(seconds=3605)


def test_get_thumbnail_url(stream: kasai.Stream) -> None:
    assert (
        stream.get_thumbnail_url(1280, 720)
        == "https://static-cdn.jtvnw.net/previews-ttv/live_user_amar-1280x720.jpg"
    )
