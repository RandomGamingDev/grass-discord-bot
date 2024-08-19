import module
from typing import Dict
from discord import Message
import re
import globs

class Count:
	def __init__(self, count: int = 1, last_responder: int = -1, record: int = 0) -> None:
		self.count: int = count
		self.last_responder: int = last_responder
		self.record: int = record

class CounterModule(module.Module):
	def __init__(self) -> None:
		super().__init__()

		# Create the table if it doesn't already exist
		globs.cursor.execute("CREATE TABLE IF NOT EXISTS counter (channel bigint PRIMARY KEY, count bigint, last_responder bigint, record bigint);")
		self.counts: Dict[int, Count] = {}

		# Write the data from the table to the module
		globs.cursor.execute("SELECT * FROM counter;")
		dataset = globs.cursor.fetchall()
		for row in dataset:
			self.counts[row[0]] = Count(*row[1:])

	async def get_res(self, msg: Message) -> str | None:
		nullable_num = re.search(r'^\d+$', msg.content)
		if nullable_num == None:
			return None
		num = nullable_num.group(0)
		
		if msg.channel.id not in self.counts:
			self.counts[msg.channel.id] = Count()
			globs.cursor.execute(
				f"INSERT INTO counter (channel, count, last_responder, record) VALUES (%s, 1, -1, 0);",
				[str(msg.channel.id)])

		count = self.counts[msg.channel.id]
		if int(num) != count.count:
			return f"❌ {msg.author.mention} messed up! The next number was {count.count}, not {num}! ❌"
		if msg.author.id == count.last_responder:
			return f"❌ {msg.author.mention} messed up! You can't count twice in a row! ❌"

		return ""
	
	async def after_res(self, usr_msg: Message, bot_msg: Message | None) -> None:
		count = self.counts[usr_msg.channel.id]
		if bot_msg is None:
			count.count += 1
			count.last_responder = usr_msg.author.id
			if count.count <= count.record:
				await usr_msg.add_reaction("✅")
			else:
				await usr_msg.add_reaction("☑️")
				count.record = count.count
		else:
			count.count = 1
			count.last_responder = -1
			await usr_msg.add_reaction("❌")

		# Update the database with the new values
		globs.cursor.execute(
			f"UPDATE counter SET count=%s, last_responder=%s, record=%s WHERE channel=%s;",
			[str(count.count), str(count.last_responder), str(count.record), str(usr_msg.channel.id)])
		globs.connection.commit()

		return None
