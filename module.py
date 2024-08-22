from discord import Message
from typing import Union

class Module:
	def __init__(self) -> None:
		pass

	async def get_res(self, msg: Message) -> Union[dict, None]:
		pass

	async def after_res(self, usr_msg: Message, bot_msg: Union[Message, None]) -> None:
		pass
