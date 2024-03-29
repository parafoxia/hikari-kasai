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

__productname__ = "hikari-kasai"
__version__ = "0.11a"
__description__ = "A bridge between Discord and Twitch chat."
__url__ = "https://github.com/parafoxia/hikari-kasai"
__docs__ = "https://parafoxia.github.io/hikari-kasai/kasai"
__author__ = "Ethan Henderson"
__author_email__ = "ethan.henderson.1998@gmail.com"
__license__ = "BSD 3-Clause 'New' or 'Revised' License"
__bugtracker__ = "https://github.com/parafoxia/hikari-kasai/issues"
__ci__ = "https://github.com/parafoxia/hikari-kasai/actions"
__changelog__ = "https://github.com/parafoxia/hikari-kasai/releases"

TWITCH_HELIX_URI = "https://api.twitch.tv/helix/"
TWITCH_TOKEN_URI = "https://id.twitch.tv/oauth2/token"  # nosec: B105

from pathlib import Path

readme = Path(__file__).parent.parent / "README.md"

# This is only needed for documentation purposes.
if readme.is_file():
    __doc__ = (
        f"### Welcome to the documentation for Kasai v{__version__}!\n\n"
        + readme.read_text()[9:]
    )

from kasai.bot import *
from kasai.channels import *
from kasai.errors import *
from kasai.events import *
from kasai.games import *
from kasai.messages import *
from kasai.streams import *
from kasai.traits import *
from kasai.twitch import *
from kasai.users import *
