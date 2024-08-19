import module
from discord import Intents, Client, Message
import random

class RandomModule(module.Module):
    def __init__(self) -> None:
        super().__init__()

    async def get_res(self, msg: Message) -> str:
        if not msg.content.startswith("!randchoice"):
            return
        return random.choice(msg.content[12:].split(';'))
