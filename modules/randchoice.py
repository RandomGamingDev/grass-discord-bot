import module
from discord import Intents, Client, Message
import random
from typing import Union

class RandomModule(module.Module):
    def __init__(self) -> None:
        super().__init__()

    async def get_res(self, msg: Message) -> Union[dict, None]:
        if not msg.content.startswith("!randchoice"):
            return
        return { "content": random.choice(msg.content[12:].split(';')) }