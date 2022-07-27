# Kasai Examples - A collection of examples for Kasai.
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

"""This example depicts a simple bot with a `!ping` command for both
Discord and Twitch."""

import os

import dotenv
import hikari

import kasai

# Load environment variables. You don't have to do it like this, but it
# makes the os.environ stuff possible. You need a .env file to do this.
dotenv.load_dotenv()

bot = kasai.GatewayBot(
    os.environ["TOKEN"],
    os.environ["IRC_TOKEN"],
    os.environ["TWITCH_CLIENT_ID"],
    os.environ["TWITCH_CLIENT_SECRET"],
)


@bot.listen()
async def on_started(_: hikari.StartedEvent) -> None:
    """Join our Twitch channel once the bot starts. We'll use the
    Twitch Developers channel for this example."""

    await bot.twitch.join("twitchdev")


@bot.listen()
async def on_message(event: hikari.MessageCreateEvent) -> None:
    """Listen for Discord messages."""

    if not event.is_human:
        # Do not respond to bots or webhooks!
        return

    if event.content == "!ping":
        await event.message.respond("Pong!")


@bot.listen()
async def on_twitch_message(event: kasai.MessageCreateEvent) -> None:
    """Listen for Twitch messages."""

    # There's no way to check for bot status using a Twitch message, and
    # this event doesn't get called at all for messages this bot sends.

    # Note how the syntax here is identical?
    if event.content == "!ping":
        await event.message.respond("Pong!")


if __name__ == "__main__":
    bot.run()
