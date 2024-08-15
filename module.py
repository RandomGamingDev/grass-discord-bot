from discord import Message

class Module:
	def __init__(self) -> None:
		pass

	async def get_res(self, msg: Message) -> str:
		return ""

	async def after_res(self, usr_msg: Message, bot_msg: Message | None) -> str:
		return ""
