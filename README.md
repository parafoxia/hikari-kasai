# Kasai

[![PyPi version](https://img.shields.io/pypi/v/hikari-kasai.svg)](https://pypi.python.org/pypi/hikari-kasai/)
[![PyPI - Status](https://img.shields.io/pypi/status/hikari-kasai)](https://pypi.python.org/pypi/hikari-kasai/)
[![Downloads](https://pepy.tech/badge/hikari-kasai)](https://pepy.tech/project/hikari-kasai)
[![GitHub last commit](https://img.shields.io/github/last-commit/parafoxia/hikari-kasai)](https://github.com/parafoxia/hikari-kasai)
[![Docs](https://img.shields.io/badge/docs-pdoc-success)](https://parafoxia.github.io/hikari-kasai/kasai/)
[![License](https://img.shields.io/github/license/parafoxia/hikari-kasai.svg)](https://github.com/parafoxia/hikari-kasai/blob/main/LICENSE)

Kasai serves as a bridge between Discord and Twitch, allowing a single bot to interact with both platforms.

This serves to extend [Hikari](https://pypi.org/project/hikari/), and cannot be used without it.

## Installation

To install the latest released version of Kasai, use the following command:
```sh
pip install hikari-kasai
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/parafoxia/hikari-kasai
```

You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.

## Creating your bot

Kasai provides a subclass for `hikari.GatewayBot` that contains methods and attributes for Twitch chat interfacing.

```py
import kasai

bot = kasai.GatewayBot(...)
```

To use Kasai with command handlers, you will need to create a custom subclass that inherits from both `kasai.GatewayBot` and your command handler's bot class.
For example, if you want to use *Lightbulb*:

```py
import kasai
import lightbulb

class Bot(kasai.GatewayBot, lightbulb.BotApp):
    ...

bot = Bot(...)
```

## Usage

A working implementation could look something like this:

```py
import os

import dotenv
import hikari
import kasai

# You will need a .env file for this.
dotenv.load_dotenv()

# Create the bot.
bot = kasai.GatewayBot(
    os.environ["TOKEN"],
    os.environ["IRC_TOKEN"],
    os.environ["TWITCH_CLIENT_ID"],
    os.environ["TWITCH_CLIENT_SECRET"],
)

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    # Connect to your Twitch chat.
    await bot.twitch.join("twitchdev")

@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent):
    # Send a message from Discord to Twitch chat.
    if event.content.startswith("!send"):
        await bot.twitch.create_message("twitchdev", event.content[6:])

@bot.listen(kasai.MessageCreateEvent)
async def on_twitch_message(event: kasai.MessageCreateEvent):
    # Basic Twitch command implementation.
    if event.content.startswith("!ping"):
        await event.message.respond("Pong!", reply=True)

# Run the bot.
bot.run()
```

There are [more examples](https://github.com/parafoxia/hikari-kasai/tree/main/examples) should you wish to see them.
It may also be worth looking into how to [speed Hikari up](https://github.com/hikari-py/hikari#making-your-application-more-efficient) to get the best performance out of Kasai.

## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/parafoxia/hikari-kasai/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/parafoxia/hikari-kasai/blob/main/CONTRIBUTING.md)

## License

The *hikari-kasai* module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/hikari-kasai/blob/main/LICENSE).
