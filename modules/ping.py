import module
from discord import Message
from typing import Union

class PingModule(module.Module):
	def __init__(self) -> None:
		super().__init__()

	async def get_res(self, msg: Message) -> Union[dict, None]:
		if msg.content != "!ping":
			return None
		return { "content": "pong!" }
	
	async def after_res(self, usr_msg: Message, bot_msg: Union[Message, None]) -> None:
		await usr_msg.add_reaction("🏓")
		await bot_msg.add_reaction("🏓")
