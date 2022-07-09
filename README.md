# Kasai

Kasai serves as a bridge between Discord and Twitch, allowing a single bot to interact with both platforms.

## Installation

To install the latest released version of *Kasai*, use the following command:
```sh
pip install hikari-kasai
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/parafoxia/hikari-kasai
```

You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.

## Creating your bot

*Kasai* provides a subclass for `hikari.GatewayBot` that contains methods and attributes for Twitch chat interfacing.

```py
import kasai

bot = kasai.GatewayBot(...)
```

To use *Kasai* with command handlers, you will need to create a custom subclass that inherits from both `kasai.GatewayBot` and your command handler's bot class.
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
)

@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event):
    if event.content == "!start":
        # Start listening for messages.
        await bot.start_irc("#channel1", "#channel2")

    elif event.content == "!close":
        # Stop listening for messages.
        await bot.close_irc()

    elif event.content.startswith("!send"):
        # Send a message to Twitch chat.
        await bot.twitch.create_message("#channel1", event.content[6:])

@bot.listen(kasai.PrivMessageCreateEvent)
async def on_twitch_message(event):
    # Display message information.
    print(f"{event.author.name} said {event.content} in {event.channel.name}")

# Run the bot.
bot.run()
```


## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/parafoxia/hikari-kasai/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/parafoxia/hikari-kasai/blob/main/CONTRIBUTING.md)

## License

The *hikari-kasai* module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/hikari-kasai/blob/main/LICENSE).
