from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import atexit
import globs

load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

import modules

async def send_msg(msg: Message) -> None:
	if not msg.content:
		print("WARNING: Message is empty most likely due to improper intents")

	for module in modules.modules:
		try:
			res = await module.get_res(msg=msg)
		except Exception as exception:
			print(f"ERROR: {module} threw the following error when responding: {exception}")
			continue
		if res != None: # If the bot replies hand over control to it
			break
	if res == None: # If no bots replyed
		return
	reply = None
	if res != "": # If the bot claimed the response and had a message to send
		reply = await msg.reply(res)
	try:
		await module.after_res(usr_msg=msg, bot_msg=reply)
	except Exception as exception:
		print(f"ERROR: {module} threw the following error after responding: {exception}")

@client.event
async def on_ready() -> None:
	print(f"{client.user} is now running!")

@client.event
async def on_message(msg: Message) -> None:
	if msg.author == client.user:
		return
	await send_msg(msg=msg)

def main() -> None:
	client.run(token=DISCORD_TOKEN)
if __name__ == "__main__":
	main()

def exit_handler():
  globs.cursor.close()
  globs.connection.close()
atexit.register(exit_handler)