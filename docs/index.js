URLS=[
"kasai/index.html",
"kasai/entity_factory.html",
"kasai/traits.html",
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
"doc":" Welcome to the documentation for Kasai v0.7a! [![PyPi version](https: img.shields.io/pypi/v/hikari-kasai.svg)](https: pypi.python.org/pypi/hikari-kasai/) [![PyPI - Status](https: img.shields.io/pypi/status/hikari-kasai)](https: pypi.python.org/pypi/hikari-kasai/) [![Downloads](https: pepy.tech/badge/hikari-kasai)](https: pepy.tech/project/hikari-kasai) [![GitHub last commit](https: img.shields.io/github/last-commit/parafoxia/hikari-kasai)](https: github.com/parafoxia/hikari-kasai) [![Docs](https: img.shields.io/badge/docs-pdoc-success)](https: parafoxia.github.io/hikari-kasai/kasai/) [![License](https: img.shields.io/github/license/parafoxia/hikari-kasai.svg)](https: github.com/parafoxia/hikari-kasai/blob/main/LICENSE) Kasai serves as a bridge between Discord and Twitch, allowing a single bot to interact with both platforms.  Installation To install the latest released version of  Kasai , use the following command:   pip install hikari-kasai   You can also install the latest development version using the following command:   pip install git+https: github.com/parafoxia/hikari-kasai   You may need to prefix these commands with a call to the Python interpreter depending on your OS and Python configuration.  Creating your bot  Kasai provides a subclass for  hikari.GatewayBot that contains methods and attributes for Twitch chat interfacing.   import kasai bot = kasai.GatewayBot( .)   To use  Kasai with command handlers, you will need to create a custom subclass that inherits from both  kasai.GatewayBot and your command handler's bot class. For example, if you want to use  Lightbulb :   import kasai import lightbulb class Bot(kasai.GatewayBot, lightbulb.BotApp):  . bot = Bot( .)    Usage A working implementation could look something like this:   import os import dotenv import hikari import kasai  You will need a .env file for this. dotenv.load_dotenv()  Create the bot. bot = kasai.GatewayBot( os.environ[\"TOKEN\"], os.environ[\"IRC_TOKEN\"], os.environ[\"TWITCH_CLIENT_ID\"], os.environ[\"TWITCH_CLIENT_SECRET\"], ) @bot.listen(hikari.StartedEvent) async def on_started(event: hikari.StartedEvent):  Connect to your Twitch chat. await bot.twitch.join(\" twitchdev\") @bot.listen(hikari.GuildMessageCreateEvent) async def on_message(event: hikari.GuildMessageCreateEvent):  Send a message from Discord to Twitch chat. if event.content.startswith(\"!send\"): await bot.twitch.create_message(\" twitchdev\", event.content[6:]) @bot.listen(kasai.MessageCreateEvent) async def on_twitch_message(event: kasai.MessageCreateEvent):  Basic Twitch command implementation. if event.content.startswith(\"!ping\"): await event.message.respond(\"Pong!\")  Run the bot. bot.run()    Contributing Contributions are very much welcome! To get started:  Familiarise yourself with the [code of conduct](https: github.com/parafoxia/hikari-kasai/blob/main/CODE_OF_CONDUCT.md)  Have a look at the [contributing guide](https: github.com/parafoxia/hikari-kasai/blob/main/CONTRIBUTING.md)  License The  hikari-kasai module for Python is licensed under the [BSD 3-Clause License](https: github.com/parafoxia/hikari-kasai/blob/main/LICENSE)."
},
{
"ref":"kasai.entity_factory",
"url":1,
"doc":""
},
{
"ref":"kasai.entity_factory.TwitchEntityFactory",
"url":1,
"doc":"Interface for components that serialize and deserialize JSON payloads."
},
{
"ref":"kasai.entity_factory.TwitchEntityFactory.deserialize_twitch_user",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactory.deserialize_twitch_viewer",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactory.deserialize_twitch_channel",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactory.deserialize_twitch_message",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactoryImpl",
"url":1,
"doc":"Standard implementation for a serializer/deserializer. This will convert objects to/from JSON compatible representations."
},
{
"ref":"kasai.entity_factory.TwitchEntityFactoryImpl.deserialize_twitch_user",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactoryImpl.deserialize_twitch_viewer",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactoryImpl.deserialize_twitch_channel",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.entity_factory.TwitchEntityFactoryImpl.deserialize_twitch_message",
"url":1,
"doc":"",
"func":1
},
{
"ref":"kasai.traits",
"url":2,
"doc":""
},
{
"ref":"kasai.traits.TwitchAware",
"url":2,
"doc":"A structural supertype for a Twitch-aware object. These are able to perform Twitch API calls and IRC operations."
},
{
"ref":"kasai.traits.TwitchAware.twitch",
"url":2,
"doc":"The Twitch client to use for Twitch operations."
},
{
"ref":"kasai.errors",
"url":3,
"doc":""
},
{
"ref":"kasai.errors.KasaiError",
"url":3,
"doc":"The base exception class for all Kasai errors."
},
{
"ref":"kasai.errors.NotAlive",
"url":3,
"doc":"Exception thrown when the Twitch client is not alive when it should be."
},
{
"ref":"kasai.errors.IsAlive",
"url":3,
"doc":"Exception thrown when the Twitch client is alive when it shouldn't be."
},
{
"ref":"kasai.errors.HelixError",
"url":3,
"doc":"Exception thrown when something goes wrong regarding the Twitch Helix API."
},
{
"ref":"kasai.errors.RequestFailed",
"url":3,
"doc":"Exception thrown when a Twitch Helix API request fails."
},
{
"ref":"kasai.errors.IrcError",
"url":3,
"doc":"Exception thrown when something goes wrong regarding IRC."
},
{
"ref":"kasai.errors.NotJoined",
"url":3,
"doc":"Exception thrown when sending a message to a channel the client has not joined."
},
{
"ref":"kasai.events",
"url":4,
"doc":""
},
{
"ref":"kasai.events.KasaiEvent",
"url":4,
"doc":"The basis for all Kasai events."
},
{
"ref":"kasai.events.KasaiEvent.app",
"url":4,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.MessageCreateEvent",
"url":4,
"doc":"Event fired when a Twitch IRC message is sent.  important This event is not triggered when your bot sends a message. Method generated by attrs for class MessageCreateEvent."
},
{
"ref":"kasai.events.MessageCreateEvent.message_id",
"url":4,
"doc":"The ID of the sent message."
},
{
"ref":"kasai.events.MessageCreateEvent.app",
"url":4,
"doc":"The base client application."
},
{
"ref":"kasai.events.MessageCreateEvent.author",
"url":4,
"doc":"The user who sent the message."
},
{
"ref":"kasai.events.MessageCreateEvent.author_id",
"url":4,
"doc":"The ID of the user who sent the message."
},
{
"ref":"kasai.events.MessageCreateEvent.channel",
"url":4,
"doc":"The channel the message was sent to."
},
{
"ref":"kasai.events.MessageCreateEvent.channel_id",
"url":4,
"doc":"The ID of the channel the message was sent to."
},
{
"ref":"kasai.events.MessageCreateEvent.bits",
"url":4,
"doc":"The number of bits the user sent in the message."
},
{
"ref":"kasai.events.MessageCreateEvent.content",
"url":4,
"doc":"The text content of the message."
},
{
"ref":"kasai.events.MessageCreateEvent.message",
"url":4,
"doc":"The message that was sent."
},
{
"ref":"kasai.events.PingEvent",
"url":4,
"doc":"Event fired when the client receives a PING message. Method generated by attrs for class PingEvent."
},
{
"ref":"kasai.events.PingEvent.app",
"url":4,
"doc":"The base client application."
},
{
"ref":"kasai.events.JoinEvent",
"url":4,
"doc":"Event fired when the client joins a Twitch channel's chat.  important To get more information about the channel, use  JoinRoomstateEvent instead. Method generated by attrs for class JoinEvent."
},
{
"ref":"kasai.events.JoinEvent.app",
"url":4,
"doc":"The base client application."
},
{
"ref":"kasai.events.JoinEvent.channel",
"url":4,
"doc":"The name of the channel the client joined."
},
{
"ref":"kasai.events.PartEvent",
"url":4,
"doc":"Event fired when the client parts (leaves) a Twitch channel's chat. Method generated by attrs for class PartEvent."
},
{
"ref":"kasai.events.PartEvent.app",
"url":4,
"doc":"The bot client instance."
},
{
"ref":"kasai.events.PartEvent.channel",
"url":4,
"doc":"The name of the channel the client parted."
},
{
"ref":"kasai.events.JoinRoomstateEvent",
"url":4,
"doc":"Event fired when the client receives ROOMSTATE information after joining a channel.  note This event contains more detailed information regarding the channel the client joined, however as that information does not always get sent from Twitch immediately, it is dispatched with a separate event. Method generated by attrs for class JoinRoomstateEvent."
},
{
"ref":"kasai.events.JoinRoomstateEvent.channel_id",
"url":4,
"doc":"The ID of the channel the client joined."
},
{
"ref":"kasai.events.JoinRoomstateEvent.app",
"url":4,
"doc":"The base client instance."
},
{
"ref":"kasai.events.JoinRoomstateEvent.game",
"url":4,
"doc":"The game the channel is currently playing (or most recently played)."
},
{
"ref":"kasai.events.JoinRoomstateEvent.game_id",
"url":4,
"doc":"The ID of the game the channel is currently playing (or most recently played)."
},
{
"ref":"kasai.events.JoinRoomstateEvent.title",
"url":4,
"doc":"The title of the channel's current (or most recent) stream."
},
{
"ref":"kasai.events.JoinRoomstateEvent.channel",
"url":4,
"doc":"The channel the client joined."
},
{
"ref":"kasai.events.ModActionEvent",
"url":4,
"doc":"Event fired when a moderation action is taken.  note This currently only supports CLEARCHAT, BAN, and TIMEOUT actions. Method generated by attrs for class ModActionEvent."
},
{
"ref":"kasai.events.ModActionEvent.channel_id",
"url":4,
"doc":"The ID of the channel."
},
{
"ref":"kasai.events.ModActionEvent.app",
"url":4,
"doc":"The base client instance."
},
{
"ref":"kasai.events.ModActionEvent.channel",
"url":4,
"doc":"The channel the mod action was performed in."
},
{
"ref":"kasai.events.ModActionEvent.created_at",
"url":4,
"doc":"The date and time the mod action was executed."
},
{
"ref":"kasai.events.ClearEvent",
"url":4,
"doc":"Event fired when a chat is cleared. Method generated by attrs for class ClearEvent."
},
{
"ref":"kasai.events.ClearEvent.channel_id",
"url":4,
"doc":"The ID of the channel."
},
{
"ref":"kasai.events.ClearEvent.app",
"url":4,
"doc":"The base client instance."
},
{
"ref":"kasai.events.ClearEvent.channel",
"url":4,
"doc":"The channel the mod action was performed in."
},
{
"ref":"kasai.events.ClearEvent.created_at",
"url":4,
"doc":"The date and time the mod action was executed."
},
{
"ref":"kasai.events.BanEvent",
"url":4,
"doc":"Event fired when a user is banned from a chat channel. Method generated by attrs for class BanEvent."
},
{
"ref":"kasai.events.BanEvent.user_id",
"url":4,
"doc":"The ID of the user that was banned."
},
{
"ref":"kasai.events.BanEvent.user",
"url":4,
"doc":"The user that was banned."
},
{
"ref":"kasai.events.BanEvent.channel_id",
"url":4,
"doc":"The ID of the channel."
},
{
"ref":"kasai.events.BanEvent.app",
"url":4,
"doc":"The base client instance."
},
{
"ref":"kasai.events.BanEvent.channel",
"url":4,
"doc":"The channel the mod action was performed in."
},
{
"ref":"kasai.events.BanEvent.created_at",
"url":4,
"doc":"The date and time the mod action was executed."
},
{
"ref":"kasai.events.TimeoutEvent",
"url":4,
"doc":"Event fired when a user is timed out from a chat channel. Method generated by attrs for class TimeoutEvent."
},
{
"ref":"kasai.events.TimeoutEvent.user_id",
"url":4,
"doc":"The ID of the user that was banned."
},
{
"ref":"kasai.events.TimeoutEvent.duration",
"url":4,
"doc":"The duration of the timeout, in seconds."
},
{
"ref":"kasai.events.TimeoutEvent.user",
"url":4,
"doc":"The user that was banned."
},
{
"ref":"kasai.events.TimeoutEvent.channel_id",
"url":4,
"doc":"The ID of the channel."
},
{
"ref":"kasai.events.TimeoutEvent.app",
"url":4,
"doc":"The base client instance."
},
{
"ref":"kasai.events.TimeoutEvent.channel",
"url":4,
"doc":"The channel the mod action was performed in."
},
{
"ref":"kasai.events.TimeoutEvent.created_at",
"url":4,
"doc":"The date and time the mod action was executed."
},
{
"ref":"kasai.channels",
"url":5,
"doc":""
},
{
"ref":"kasai.channels.Game",
"url":5,
"doc":"A class representing a Twitch game. Method generated by attrs for class Game."
},
{
"ref":"kasai.channels.Game.id",
"url":5,
"doc":"This game's ID."
},
{
"ref":"kasai.channels.Game.name",
"url":5,
"doc":"This game's name."
},
{
"ref":"kasai.channels.Channel",
"url":5,
"doc":"A class representing a Twitch channel. Method generated by attrs for class Channel."
},
{
"ref":"kasai.channels.Channel.irc_format",
"url":5,
"doc":"This channel's username in the format IRC expects it."
},
{
"ref":"kasai.channels.Channel.send",
"url":5,
"doc":"Send a message to this channel. Example    -   >>> await channel.send(\"Never gonna give you up!\")   Parameters      content : str The text content of the message you want to send. Returns    - None",
"func":1
},
{
"ref":"kasai.channels.Channel.app",
"url":5,
"doc":"The base client application."
},
{
"ref":"kasai.channels.Channel.delay",
"url":5,
"doc":"The number of seconds this channel's stream is delayed by."
},
{
"ref":"kasai.channels.Channel.display_name",
"url":5,
"doc":"The name this channel is displayed as on Twitch. This will always be the username with casing variations."
},
{
"ref":"kasai.channels.Channel.game",
"url":5,
"doc":"The game this channel is playing."
},
{
"ref":"kasai.channels.Channel.id",
"url":5,
"doc":"This channel's ID."
},
{
"ref":"kasai.channels.Channel.language",
"url":5,
"doc":"The language this channel is streaming using (according to their settings)."
},
{
"ref":"kasai.channels.Channel.title",
"url":5,
"doc":"The title of this channel's stream."
},
{
"ref":"kasai.channels.Channel.username",
"url":5,
"doc":"This channel's login username."
},
{
"ref":"kasai.bot",
"url":6,
"doc":""
},
{
"ref":"kasai.bot.GatewayBot",
"url":6,
"doc":"A class representing a Discord bot. This extends  hikari.GatewayBot . To extend command handler classes, you should create a subclass that inherits from this class and your preferred command handler's bot class (making sure you inherit from this class first). Example:   class MyBot(kasai.GatewayBot, lightbulb.BotApp):  . bot = MyBot( .)   Parameters      token : str Your Discord bot's token. irc_token : str Your Twitch IRC access token. This is different to an API access token. client_id : str Your Twitch application's client ID. client_secret : str Your Twitch application's client secret. Other Parameters         banner : str The banner to be displayed on boot (this is passed directly to the superclass initialiser). This defaults to \"kasai\".  kwargs : Any Additional keyword arguments to be passed to the superclasses."
},
{
"ref":"kasai.bot.GatewayBot.entity_factory",
"url":6,
"doc":"This client's entity factory. Returns    - kasai.entity_factory.TwitchEntityFactory"
},
{
"ref":"kasai.bot.GatewayBot.twitch",
"url":6,
"doc":"The Twitch client. Returns    - kasai.twitch.TwitchClient"
},
{
"ref":"kasai.bot.GatewayBot.start",
"url":6,
"doc":"Starts the Twitch and Discord clients (in that order). This often does not need to be called, as  kasai.GatewayBot.run will call this automatically. Other Parameters          kwargs : Any Additional arguments to be passed to  hikari.GatewayBot.start .",
"func":1
},
{
"ref":"kasai.bot.GatewayBot.print_banner",
"url":6,
"doc":"Print the banner. This allows library vendors to override this behaviour, or choose to inject their own \"branding\" on top of what hikari provides by default. Normal users should not need to invoke this function, and can simply change the  banner argument passed to the constructor to manipulate what is displayed. Parameters      banner : typing.Optional[builtins.str] The package to find a  banner.txt in. allow_color : builtins.bool A flag that allows advising whether to allow color if supported or not. Can be overridden by setting a  \"CLICOLOR\" environment variable to a non- \"0\" string. force_color : builtins.bool A flag that allows forcing color to always be output, even if the terminal device may not support it. Setting the  \"CLICOLOR_FORCE\" environment variable to a non- \"0\" string will override this.  ! note  force_color will always take precedence over  allow_color . extra_args : typing.Optional[typing.Dict[builtins.str, builtins.str If provided, extra $-substitutions to use when printing the banner. Default substitutions can not be overwritten. Raises    builtins.ValueError If  extra_args contains a default $-substitution.",
"func":1
},
{
"ref":"kasai.ux",
"url":7,
"doc":""
},
{
"ref":"kasai.ux.display_splash",
"url":7,
"doc":"",
"func":1
},
{
"ref":"kasai.ux.deprecated",
"url":7,
"doc":"",
"func":1
},
{
"ref":"kasai.ux.depr_warn",
"url":7,
"doc":"",
"func":1
},
{
"ref":"kasai.twitch",
"url":8,
"doc":""
},
{
"ref":"kasai.twitch.TwitchClient",
"url":8,
"doc":"A class representing a Twitch client. Parameters      app : kasai.GatewayBot The base client application. irc_token : str Your Twitch IRC access token. This is different to an API access token. client_id : str Your Twitch application's client ID. client_secret : str Your Twitch application's client secret."
},
{
"ref":"kasai.twitch.TwitchClient.is_alive",
"url":8,
"doc":"Whether the client is connected to the Twitch Helix API. This does not necessarily mean the client is connected to the Twitch IRC servers."
},
{
"ref":"kasai.twitch.TwitchClient.is_authorised",
"url":8,
"doc":"Whether the client is authorised to connect to the Twitch Helix API."
},
{
"ref":"kasai.twitch.TwitchClient.app",
"url":8,
"doc":"The base client application."
},
{
"ref":"kasai.twitch.TwitchClient.start",
"url":8,
"doc":"Start all Twitch services. This is called automatically when the Discord bot starts. Returns    - None",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.close",
"url":8,
"doc":"Ends all Twitch services. This is called automatically when the Discord bot shuts down. Returns    - None",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.join",
"url":8,
"doc":"Joins the given Twitch channels' chats. Example    -   >>> await bot.twitch.join(\"twitch\", \"twitchdev\")   Example    -   >>> channels = (\"twitch\", \"twitchdev\") >>> await bot.twitch.join( channels)   Parameters       channels : str The login usernames of the channels to join. Returns    - None",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.part",
"url":8,
"doc":"Parts (leaves) the given Twitch channels' chats.  note You do not need to part joined channels before shutting the bot down \u2014 this is handled automatically. Example    -   >>> await bot.twitch.part(\"twitch\", \"twitchdev\")   Example    -   >>> channels = (\"twitch\", \"twitchdev\") >>> await bot.twitch.part( channels)   Parameters       channels : str The login usernames of the channels to part. Returns    - None",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.create_message",
"url":8,
"doc":"Send a message to a Twitch channel. Example    -   >>> await bot.twitch.create_message( \"twitchdev\", \"Never gonna give you up!\", )   Parameters      channel : str The login username of the channel you want to send a message to. content : str The text content of the message you want to send. Returns    - None",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.fetch_user",
"url":8,
"doc":"Fetches a user from the Twitch Helix API. Example    -   >>> user1 = await bot.twitch.fetch_user(\"twitchdev\") >>> user2 = await bot.twitch.fetch_user(\"141981764\") >>> user1  user2 True   Parameters      user : str The login username or the ID of the user to fetch. Note that while Twitch user IDs are numerical, they are strings. Returns    - kasai.User The fetched user.",
"func":1
},
{
"ref":"kasai.twitch.TwitchClient.fetch_channel",
"url":8,
"doc":"Fetches a channel from the Twitch Helix API. Example    -   >>> channel = await bot.twitch.fetch_channel(\"141981764\") >>> print(channel.username) twitchdev   Parameters      channel : str The ID of the channel to fetch. Note that while Twitch channel IDs are numerical, they are strings. A channel's ID is identical to the user ID of the channel. Returns    - kasai.Channel The fetched channel.",
"func":1
},
{
"ref":"kasai.messages",
"url":9,
"doc":""
},
{
"ref":"kasai.messages.Message",
"url":9,
"doc":"A class representing a Twitch IRC PRIVMSG. Method generated by attrs for class Message."
},
{
"ref":"kasai.messages.Message.respond",
"url":9,
"doc":"Send a message to this channel this message was sent to. Example    -   >>> await message.respond(\"Never gonna give you up!\")   Parameters      content : str The text content of the message you want to send. Returns    - None",
"func":1
},
{
"ref":"kasai.messages.Message.app",
"url":9,
"doc":"The base client application."
},
{
"ref":"kasai.messages.Message.author",
"url":9,
"doc":"The user who sent this message."
},
{
"ref":"kasai.messages.Message.bits",
"url":9,
"doc":"The number of bits the user sent in this message."
},
{
"ref":"kasai.messages.Message.channel",
"url":9,
"doc":"The channel this message was sent to "
},
{
"ref":"kasai.messages.Message.content",
"url":9,
"doc":"The text content of this message."
},
{
"ref":"kasai.messages.Message.created_at",
"url":9,
"doc":"The date and time this message was sent."
},
{
"ref":"kasai.messages.Message.id",
"url":9,
"doc":"This message's ID."
},
{
"ref":"kasai.users",
"url":10,
"doc":""
},
{
"ref":"kasai.users.User",
"url":10,
"doc":"A class representing a Twitch user."
},
{
"ref":"kasai.users.User.app",
"url":10,
"doc":"Client application that models may use for procedures."
},
{
"ref":"kasai.users.User.broadcaster_type",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.description",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.display_name",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.id",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.username",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.offline_image_url",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.profile_image_url",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.type",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.User.created_at",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer",
"url":10,
"doc":"A class representing a Twitch viewer. This is largely the same as a normal  User , but contains additional information related to the user's relationship with the channel they're currently viewing."
},
{
"ref":"kasai.users.Viewer.color",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.colour",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.is_mod",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.is_subscriber",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.is_turbo",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.is_broadcaster",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.app",
"url":10,
"doc":"Client application that models may use for procedures."
},
{
"ref":"kasai.users.Viewer.broadcaster_type",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.description",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.display_name",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.id",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.username",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.offline_image_url",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.profile_image_url",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.type",
"url":10,
"doc":"A property."
},
{
"ref":"kasai.users.Viewer.created_at",
"url":10,
"doc":"A property."
}
]