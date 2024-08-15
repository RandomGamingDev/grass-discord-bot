# Grass Bot
### A discord bot created to have random modules added to it however you'd like, whether for just yourself or for friends as well it's a great coding experience for all :D

## Instructions
All modules need to be classes that inherit from the `Module` class which is located in `module.py` and to enable them they must be in the `modules` list in `modules.py`.
The order of modules in the `modules` list does matter, since each user message can only have 1 module which is allowed to take control/priority to respond via the default system and deciding which bots can take control/priority before which other modules is based on the ranking which goes from `0` -> `len(modules) - 1` in order.

The `Module` class has 1 constructor and 2 overridable methods:
- `get_res(self, msg: discord.Message) -> str`: Gets executed upon user message event unless priority/control is taken before it arrives in the hands of the module. If the module returns `None` priority/control keeps on getting passed on to the following modules; if it returns an empty string control is taken by the module, but nothing gets sent; and if a non-empty string gets sent control is taken by the module and the string is sent as a message
- `after_res(self, usr_msg: discord.Message, bot_msg: discord.Message) -> None`: If the module took control this will be called after the control is taken and the message is sent if there was a message sent.

The database used for storing everything is `PostgresSQL` which is also my favorite database :D

For the postgres database ofc give the permissions needed for the modules to do whatever they need to do and make sure to practice proper SQL hygiene.

## Examples
- `ping.py`: Responds to `!ping` with `pong!` and reacting both messages to demonstrate the basics.
- `counter.py`: A basic counter bot that takes the first found number, keeps tracks of records (it responds to wrong counts with ❌, record breaking counts with ☑️, and regular valid counts with ✅) by storing the current `count` (The next number needed), `last_responder` (The last person to respond), and `record` (The record that's been gotten to). This module also uses Postgres to avoid save it when the bot is rebooted.