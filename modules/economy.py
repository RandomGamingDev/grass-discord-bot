import typing
from enum import Enum
from discord import Intents, Client, Message, TextChannel
import globs
import module
from shared.economydata import EconomyInstance

class EconomyModule(module.Module):
    """Handles generic economy based commands"""
    async def get_res(self, msg:Message) -> str:
        class CommandTypes(Enum):
            """All valid economy command types"""
            BALANCE = "balance"
        user_id = msg.author.id
        valid_commands = {member.value for member in CommandTypes}
        msg_set = set(msg.content.lower().split())
        if "!economy" not in msg.content.lower() or valid_commands.isdisjoint(msg_set):
            return
        if CommandTypes.BALANCE.value in msg_set:
            user_balance = EconomyInstance.get_balance(user_id)
            return f"Balance: {user_balance}"
        return