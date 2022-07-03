# hikari-kasai

A bridge between Discord and Twitch chat.

## Installation

To install the latest stable version of *hikari-kasai*, use the following command:
```sh
pip install hikari-kasai
```

You can also install the latest development version using the following command:
```sh
pip install git+https://github.com/parafoxia/hikari-kasai
```

You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.

## Usage

All methods relating to Twitch can be accessed through `bot.irc`.

*hikari-kasai* officially supports Hikari, as well as the Lightbulb and Crescent command handlers:

```py
kasai.GatewayApp(...)
kasai.LightbulbApp(...)
kasai.CrescentApp(...)
```

However, you can use *hikari-kasai*, with any command handler you like, so long as it doesn't conflict.
To do this, you can create a subclassed bot:

```py
import kasai
import lightbulb


class Bot(kasai.GatewayApp, lightbulb.BotApp):
    ...


bot = Bot(...)
```

Providing you inherit from `GatewayApp` first, you do not need to provide an `__init__`.

A full working implementation could look something like this:

```py
import hikari
import kasai

# This can also be LightbulbApp or CrescentApp.
bot = kasai.GatewayApp(
    discord_token,
    irc_token,
    channel,
    nickname,
    **[kwargs for superclass],
)


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event):
    if event.content == "start":
        await bot.start_irc()

    elif event.content == "close":
        await bot.close_irc()

    elif event.content.startswith("send"):
        await bot.irc.create_message(event.content[5:])


@bot.listen(kasai.IrcMessageCreateEvent)
async def on_irc_message(event):
    print(f"{event.user} said: {event.content}")


bot.run()
```


## Contributing

Contributions are very much welcome! To get started:

* Familiarise yourself with the [code of conduct](https://github.com/parafoxia/hikari-kasai/blob/main/CODE_OF_CONDUCT.md)
* Have a look at the [contributing guide](https://github.com/parafoxia/hikari-kasai/blob/main/CONTRIBUTING.md)

## License

The *hikari-kasai* module for Python is licensed under the [BSD 3-Clause License](https://github.com/parafoxia/hikari-kasai/blob/main/LICENSE).
