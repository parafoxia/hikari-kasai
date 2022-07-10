URLS=[
"kasai/index.html",
"kasai/errors.html",
"kasai/events.html",
"kasai/channels.html",
"kasai/bot.html",
"kasai/ux.html",
"kasai/twitch.html",
"kasai/messages.html",
"kasai/users.html"
];
INDEX=[
{
"ref":"kasai",
"url":0,
"doc":" Welcome to the documentation for Kasai v0.6a! [![PyPi version](https: img.shields.io/pypi/v/hikari-kasai.svg)](https: pypi.python.org/pypi/hikari-kasai/) [![PyPI - Status](https: img.shields.io/pypi/status/hikari-kasai)](https: pypi.python.org/pypi/hikari-kasai/) [![Downloads](https: pepy.tech/badge/hikari-kasai)](https: pepy.tech/project/hikari-kasai) [![GitHub last commit](https: img.shields.io/github/last-commit/parafoxia/hikari-kasai)](https: github.com/parafoxia/hikari-kasai) [![Docs](https: img.shields.io/badge/docs-pdoc-success)](https: parafoxia.github.io/hikari-kasai/kasai/) [![License](https: img.shields.io/github/license/parafoxia/hikari-kasai.svg)](https: github.com/parafoxia/hikari-kasai/blob/main/LICENSE) Kasai serves as a bridge between Discord and Twitch, allowing a single bot to interact with both platforms.  Installation To install the latest released version of  Kasai , use the following command:   pip install hikari-kasai   You can also install the latest development version using the following command:   pip install git+https: github.com/parafoxia/hikari-kasai   You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.  Creating your bot  Kasai provides a subclass for  hikari.GatewayBot that contains methods and attributes for Twitch chat interfacing.   import kasai bot = kasai.GatewayBot( .)   To use  Kasai with command handlers, you will need to create a custom subclass that inherits from both  kasai.GatewayBot and your command handler's bot class. For example, if you want to use  Lightbulb :   import kasai import lightbulb class Bot(kasai.GatewayBot, lightbulb.BotApp):  . bot = Bot( .)    Usage A working implementation could look something like this:   import os import dotenv import hikari import kasai  You will need a .env file for this. dotenv.load_dotenv()  Create the bot. bot = kasai.GatewayBot( os.environ[\"TOKEN\"], os.environ[\"IRC_TOKEN\"], ) @bot.listen(hikari.GuildMessageCreateEvent) async def on_message(event): if event.content  \"!start\":  Start listening for messages. await bot.start_irc(\" channel1\", \" channel2\") elif event.content  \"!close\":  Stop listening for messages. await bot.close_irc() elif event.content.startswith(\"!send\"):  Send a message to Twitch chat. await bot.twitch.create_message(\" channel1\", event.content[6:]) @bot.listen(kasai.PrivMessageCreateEvent) async def on_twitch_message(event):  Display message information. print(f\"{event.author.name} said {event.content} in {event.channel.name}\")  Run the bot. bot.run()    Contributing Contributions are very much welcome! To get started:  Familiarise yourself with the [code of conduct](https: github.com/parafoxia/hikari-kasai/blob/main/CODE_OF_CONDUCT.md)  Have a look at the [contributing guide](https: github.com/parafoxia/hikari-kasai/blob/main/CONTRIBUTING.md)  License The  hikari-kasai module for Python is licensed under the [BSD 3-Clause License](https: github.com/parafoxia/hikari-kasai/blob/main/LICENSE)."
},
{
"ref":"kasai.errors",
"url":1,
"doc":""
},
{
"ref":"kasai.errors.KasaiError",
"url":1,
"doc":"The base exception class for all Kasai errors."
},
{
"ref":"kasai.errors.NotConnected",
"url":1,
"doc":"Exception thrown when operations that require the client to be connected are attempted without the connection."
},
{
"ref":"kasai.errors.AlreadyConnected",
"url":1,
"doc":"Exception thrown when connection operations are attempted when the client is already connected."
},
{
"ref":"kasai.events",
"url":2,
"doc":""
},
{
"ref":"kasai.events.KasaiEvent",
"url":2,
"doc":"A dataclass representing a Kasai event. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class KasaiEvent."
},
{
"ref":"kasai.events.KasaiEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.PrivMessageCreateEvent",
"url":2,
"doc":"A dataclass created whenever the client receives a new Twitch chat message. All instance attributes must be passed to the constructor on creation.  important This event is not triggered when your bot sends a message. Method generated by attrs for class PrivMessageCreateEvent."
},
{
"ref":"kasai.events.PrivMessageCreateEvent.author",
"url":2,
"doc":"The message's author. Returns    - kasai.users.User"
},
{
"ref":"kasai.events.PrivMessageCreateEvent.channel",
"url":2,
"doc":"The channel the message was sent to. Returns    - kasai.channels.Channel"
},
{
"ref":"kasai.events.PrivMessageCreateEvent.content",
"url":2,
"doc":"The content of the message. Returns    - builtins.str"
},
{
"ref":"kasai.events.PrivMessageCreateEvent.message",
"url":2,
"doc":"The message that was sent."
},
{
"ref":"kasai.events.PrivMessageCreateEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.PingEvent",
"url":2,
"doc":"A dataclass created whenever the client receives a PING message from the Twitch server. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class PingEvent."
},
{
"ref":"kasai.events.PingEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.JoinEvent",
"url":2,
"doc":"A dataclass created whenever the client joins a Twitch channel. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class JoinEvent."
},
{
"ref":"kasai.events.JoinEvent.channel_name",
"url":2,
"doc":"The name of the channel which was joined. Returns    - builtins.str"
},
{
"ref":"kasai.events.JoinEvent.message",
"url":2,
"doc":"A representation of a JOIN message."
},
{
"ref":"kasai.events.JoinEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.PartEvent",
"url":2,
"doc":"A dataclass created whenever the client parts a Twitch channel. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class PartEvent."
},
{
"ref":"kasai.events.PartEvent.channel_name",
"url":2,
"doc":"The name of the channel which was parted. Returns    - builtins.str"
},
{
"ref":"kasai.events.PartEvent.message",
"url":2,
"doc":"A representation of a PART message."
},
{
"ref":"kasai.events.PartEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.ClearEvent",
"url":2,
"doc":"A dataclass created whenever a clear command is sent to the Twitch channel. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class ClearEvent."
},
{
"ref":"kasai.events.ClearEvent.message",
"url":2,
"doc":"A representation of a CLEARCHAT message."
},
{
"ref":"kasai.events.ClearEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.BanEvent",
"url":2,
"doc":"A dataclass created whenever a ban command is sent to the Twitch channel. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class BanEvent."
},
{
"ref":"kasai.events.BanEvent.target_id",
"url":2,
"doc":"The target user's ID. Returns    - builtins.str"
},
{
"ref":"kasai.events.BanEvent.message",
"url":2,
"doc":"A representation of a CLEARCHAT message."
},
{
"ref":"kasai.events.BanEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.TimeoutEvent",
"url":2,
"doc":"A dataclass created whenever a timeout command is sent to the Twitch channel. All instance attributes must be passed to the constructor on creation. Method generated by attrs for class TimeoutEvent."
},
{
"ref":"kasai.events.TimeoutEvent.target_id",
"url":2,
"doc":"The target user's ID. Returns    - builtins.str"
},
{
"ref":"kasai.events.TimeoutEvent.duration",
"url":2,
"doc":"The timeout duration. Returns    - builtins.int"
},
{
"ref":"kasai.events.TimeoutEvent.message",
"url":2,
"doc":"A representation of a CLEARCHAT message."
},
{
"ref":"kasai.events.TimeoutEvent.app",
"url":2,
"doc":"The bot client instance."
},
{
"ref":"kasai.channels",
"url":3,
"doc":""
},
{
"ref":"kasai.channels.Channel",
"url":3,
"doc":"A dataclass representing a Twitch channel. All attributes must be passed to the constructor on creation, though you should never need to create this yourself. Method generated by attrs for class Channel."
},
{
"ref":"kasai.channels.Channel.id",
"url":3,
"doc":"The channel's ID."
},
{
"ref":"kasai.channels.Channel.name",
"url":3,
"doc":"The name of the channel."
},
{
"ref":"kasai.bot",
"url":4,
"doc":""
},
{
"ref":"kasai.bot.GatewayBot",
"url":4,
"doc":"A subclass of  hikari.impl.bot.GatewayBot which includes Twitch functionality. If you wish to use a command handler, you can create a subclass which inherits from this class and your preferred command handler's bot class. Note that if you do this, Kasai's GatewayBot  must be inherited first. For example:   class Bot(kasai.GatewayBot, lightbulb.BotApp):  . bot = Bot( .)   Parameters      token : builtins.str Your Discord bot's token. irc_token : builtins.str Your Twitch IRC access token. Other Parameters         banner : str The banner to be displayed on boot (this is passed directly to the superclass initialiser). This defaults to \"kasai\".  kwargs : Any Additional keyword arguments to be passed to the superclass.  versionchanged 0.6a  This no longer takes  channel and  nickname arguments.  You can now choose the banner that will be displayed on boot."
},
{
"ref":"kasai.bot.GatewayBot.twitch",
"url":4,
"doc":"The Twitch IRC client interface. Returns    - kasai.twitch.TwitchClient"
},
{
"ref":"kasai.bot.GatewayBot.start_irc",
"url":4,
"doc":"Create a websocket connection to Twitch's IRC servers and start listening for messages. Parameters       channels : builtins.str The channels to join once connected. This can be empty, in which case you will need to manually join your channel(s) later. All channels must be prefixed with a hash ( ). Raises    kasai.errors.AlreadyConnected Kasai is already connected to a Twitch channel.",
"func":1
},
{
"ref":"kasai.bot.GatewayBot.close_irc",
"url":4,
"doc":"Stop listening for messages and close the connection to your Twitch channel(s). Raises    kasai.errors.NotConnected Kasai is not currently connected to a Twitch channel.",
"func":1
},
{
"ref":"kasai.bot.GatewayBot.print_banner",
"url":4,
"doc":"Print the banner. This allows library vendors to override this behaviour, or choose to inject their own \"branding\" on top of what hikari provides by default. Normal users should not need to invoke this function, and can simply change the  banner argument passed to the constructor to manipulate what is displayed. Parameters      banner : typing.Optional[builtins.str] The package to find a  banner.txt in. allow_color : builtins.bool A flag that allows advising whether to allow color if supported or not. Can be overridden by setting a  \"CLICOLOR\" environment variable to a non- \"0\" string. force_color : builtins.bool A flag that allows forcing color to always be output, even if the terminal device may not support it. Setting the  \"CLICOLOR_FORCE\" environment variable to a non- \"0\" string will override this.  ! note  force_color will always take precedence over  allow_color . extra_args : typing.Optional[typing.Dict[builtins.str, builtins.str If provided, extra $-substitutions to use when printing the banner. Default substitutions can not be overwritten. Raises    builtins.ValueError If  extra_args contains a default $-substitution.",
"func":1
},
{
"ref":"kasai.ux",
"url":5,
"doc":""
},
{
"ref":"kasai.ux.display_splash",
"url":5,
"doc":"",
"func":1
},
{
"ref":"kasai.ux.deprecated",
"url":5,
"doc":"",
"func":1
},
{
"ref":"kasai.ux.depr_warn",
"url":5,
"doc":"",
"func":1
},
{
"ref":"kasai.twitch",
"url":6,
"doc":""
},
{
"ref":"kasai.twitch.TwitchClient",
"url":6,
"doc":"A class for interacting with Twitch. This is available through :obj: kasai.bot.GatewayBot.twitch , and should never need to be manually instantiated. Parameters      bot : kasai.bot.GatewayBot The Discord bot instance. token : builtins.str Your Twitch IRC token"
},
{
"ref":"kasai.twitch.TwitchClient.is_alive",
"url":6,
"doc":"Whether the websocket is open. This does not necessarily mean it's connected to a channel. Returns    - builtins.bool"
},
{
"ref":"kasai.twitch.TwitchClient.channels",
"url":6,
"doc":"A list of channels the client is connected to. Returns    - builtins.list[builtins.str]"
},
{
"ref":"kasai.twitch.TwitchClient.join",
"url":6,
"doc":"Join a Twitch channel. Parameters       channels : str The channels to join. This can be empty, in which case, nothing will happen. Raises    kasai.errors.NotConnected The client is not connected to Twitch.",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.part",
"url":6,
"doc":"Part (or leave) a Twitch channel. Parameters       channels : builtins.str The channels to part. This can be empty, in which case, nothing will happen. Raises    kasai.errors.NotConnected The client is not connected to Twitch.",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.create_message",
"url":6,
"doc":"Send a message to a given channel's chat. The client must have joined that channel to send a message. Parameters      channel : builtins.str The channel to send the message to. This must be prefixed with a hash ( ). contents : builtins.str The content of the message. The maximum allowed message length varies on a number of factors, but generally, messages should not be longer than about 400 characters. Raises    kasai.errors.NotConnected The client is not connected to a Twitch channel.",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.bot",
"url":6,
"doc":"The Discord bot instance."
},
{
"ref":"kasai.messages",
"url":7,
"doc":""
},
{
"ref":"kasai.messages.PrivMessage",
"url":7,
"doc":"A dataclass representing a PRIVMSG message. All attributes must be passed to the constructor on creation, though you should never need to create this yourself. Method generated by attrs for class PrivMessage."
},
{
"ref":"kasai.messages.PrivMessage.new",
"url":7,
"doc":"Create a new instance from raw (decoded) message data.  note The message data  must be decoded before being passed. Parameters      data : builtins.str The raw (decoded) message data. Returns    - kasai.messages.PrivMessage",
"func":1
},
{
"ref":"kasai.messages.PrivMessage.author",
"url":7,
"doc":"The author of the message."
},
{
"ref":"kasai.messages.PrivMessage.bits",
"url":7,
"doc":"The number of bits cheered in the message."
},
{
"ref":"kasai.messages.PrivMessage.channel",
"url":7,
"doc":"The channel the message was sent in."
},
{
"ref":"kasai.messages.PrivMessage.content",
"url":7,
"doc":"The content of the message."
},
{
"ref":"kasai.messages.PrivMessage.created_at",
"url":7,
"doc":"The date and time the message was sent."
},
{
"ref":"kasai.messages.PrivMessage.id",
"url":7,
"doc":"The message's unique ID."
},
{
"ref":"kasai.messages.JoinMessage",
"url":7,
"doc":"A dataclass representing a JOIN message. All attributes must be passed to the constructor on creation, though you should never need to create this yourself. Method generated by attrs for class JoinMessage."
},
{
"ref":"kasai.messages.JoinMessage.new",
"url":7,
"doc":"Create a new instance from raw (decoded) message data.  note The message data  must be decoded before being passed. Parameters      data : builtins.str The raw (decoded) message data. Returns    - kasai.messages.JoinMessage",
"func":1
},
{
"ref":"kasai.messages.JoinMessage.channel_name",
"url":7,
"doc":"The name of the channel which was joined."
},
{
"ref":"kasai.messages.PartMessage",
"url":7,
"doc":"A dataclass representing a PART message. All attributes must be passed to the constructor on creation, though you should never need to create this yourself. Method generated by attrs for class PartMessage."
},
{
"ref":"kasai.messages.PartMessage.new",
"url":7,
"doc":"Create a new instance from raw (decoded) message data.  note The message data  must be decoded before being passed. Parameters      data : builtins.str The raw (decoded) message data. Returns    - kasai.messages.PartMessage",
"func":1
},
{
"ref":"kasai.messages.PartMessage.channel_name",
"url":7,
"doc":"The name of the channel which was joined."
},
{
"ref":"kasai.messages.ModActionMessage",
"url":7,
"doc":"A dataclass representing a CLEARCHAT message. All attributes must be passed to the constructor on creation, though you should never need to create this yourself.  important This is triggered whenever a mod in your chat executes one of the following moderation actions:  /clear  /ban  /timeout This is always sent as a CLEARCHAT message regardless of the action taken. Action reasons are also not collected by this class. Method generated by attrs for class ModActionMessage."
},
{
"ref":"kasai.messages.ModActionMessage.new",
"url":7,
"doc":"Create a new instance from raw (decoded) message data.  note The message data  must be decoded before being passed. Parameters      data : builtins.str The raw (decoded) message data. Returns    - kasai.messages.ModActionMessage",
"func":1
},
{
"ref":"kasai.messages.ModActionMessage.channel",
"url":7,
"doc":"The channel the command was executed in."
},
{
"ref":"kasai.messages.ModActionMessage.command",
"url":7,
"doc":"The command that was executed."
},
{
"ref":"kasai.messages.ModActionMessage.created_at",
"url":7,
"doc":"The time the command was executed."
},
{
"ref":"kasai.messages.ModActionMessage.duration",
"url":7,
"doc":"The duration of the action. This is only non-zero if the command was a timeout, in which case it will be the number of seconds the user is timed out for."
},
{
"ref":"kasai.messages.ModActionMessage.target_id",
"url":7,
"doc":"The target user's ID. This is  None if a clear command was sent."
},
{
"ref":"kasai.users",
"url":8,
"doc":""
},
{
"ref":"kasai.users.User",
"url":8,
"doc":"A dataclass representing a Twitch user. All attributes must be passed to the constructor on creation, though you should never need to create this yourself.  note This does not necessarily represent a global user. The values of some attributes are dependent on context, often the channel the user was in when they sent a message. Method generated by attrs for class User."
},
{
"ref":"kasai.users.User.username",
"url":8,
"doc":"The user's username. This is always their display name in all lower case. Returns    - builtins.str"
},
{
"ref":"kasai.users.User.colour",
"url":8,
"doc":"An alias for those who can spell correctly. This is an integer representation of the colour's hex code. Returns    - builtins.int"
},
{
"ref":"kasai.users.User.color",
"url":8,
"doc":"The user's colour in the current context. This is an integer representation of the colour's hex code."
},
{
"ref":"kasai.users.User.display_name",
"url":8,
"doc":"The user's display name."
},
{
"ref":"kasai.users.User.id",
"url":8,
"doc":"The user's ID."
},
{
"ref":"kasai.users.User.is_broadcaster",
"url":8,
"doc":"Whether the user is the broadcaster."
},
{
"ref":"kasai.users.User.is_mod",
"url":8,
"doc":"Whether the user is a mod in the current context."
},
{
"ref":"kasai.users.User.is_subscriber",
"url":8,
"doc":"Whether the user is a subscriber in the current context."
},
{
"ref":"kasai.users.User.is_turbo",
"url":8,
"doc":"Whether the user has ads turned off globally."
},
{
"ref":"kasai.users.User.type",
"url":8,
"doc":"The user type. This will be :obj: UserType.NORMAL unless the user works for Twitch."
}
]