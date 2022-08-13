# Kasai Examples - A collection of examples for Kasai.
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.

"""This example depicts a more advanced bot that uses the Lightbulb
command handler as well as Kasai's Twitch integration."""

import os

import dotenv
import hikari
import lightbulb

import kasai

# Load environment variables. You don't have to do it like this, but it
# makes the os.environ stuff possible. You need a .env file to do this.
dotenv.load_dotenv()


class MyBot(kasai.GatewayBot, lightbulb.BotApp):
    ...


bot = MyBot(
    os.environ["TOKEN"],
    os.environ["IRC_TOKEN"],
    os.environ["TWITCH_CLIENT_ID"],
    os.environ["TWITCH_CLIENT_SECRET"],
    default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    help_slash_command=True,
)


@bot.listen()
async def on_started(_: hikari.StartedEvent) -> None:
    """Join our Twitch channel once the bot starts. We'll use the
    Twitch Developers channel for this example."""

    await bot.twitch.join("twitchdev")


@bot.command()
@lightbulb.option("text", "The text to send to Twitch.")
@lightbulb.command("send", "Send a message to Twitch!")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_send(ctx: lightbulb.SlashContext) -> None:
    """A simple slash command which sends a message to a Twitch
    channel."""

    await bot.twitch.create_message("twitchdev", ctx.options.text)


@bot.listen()
async def on_twitch_message(event: kasai.MessageCreateEvent) -> None:
    """Kasai doesn't have a command handler yet, so you'll need to use
    an event listener like this one to respond to commands. This
    particular one does exactly the same as above, just the other way
    round."""

    if not event.content.startswith("!send"):
        return

    await bot.rest.create_message(
        int(os.environ["TWITCH_LOGS_CHANNEL_ID"]), event.content[6:]
    )


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.run()
