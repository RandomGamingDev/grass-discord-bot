from discord import Intents, Client, Message
import psycopg

class Module:
	def __init__(self) -> None:
		pass

	async def get_res(self, msg: Message) -> str:
		pass

	async def after_res(self, usr_msg: Message, bot_msg: Message) -> None:
		pass