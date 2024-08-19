import module
from discord import Message

class PingModule(module.Module):
	def __init__(self) -> None:
		super().__init__()

	async def get_res(self, msg: Message) -> str | None:
		if msg.content != "!ping":
			return None
		return "pong!"
	
	async def after_res(self, usr_msg: Message, bot_msg: Message | None) -> None:
		await usr_msg.add_reaction("🏓")
		await bot_msg.add_reaction("🏓")
