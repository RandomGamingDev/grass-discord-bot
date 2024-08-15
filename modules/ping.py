import module
from discord import Message

class PingModule(module.Module):
	def __init__(self) -> None:
		super().__init__()

	async def get_res(self, msg: Message) -> str:
		if msg.content != "!ping":
			return ""
		return "pong!"
	
	async def after_res(self, usr_msg: Message, bot_msg: Message | None) -> str:
		await usr_msg.add_reaction("🏓")
		await bot_msg.add_reaction("🏓")
		return ""
