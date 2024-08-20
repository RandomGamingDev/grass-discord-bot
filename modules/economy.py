import typing
from enum import Enum
from discord import Intents, Client, Message, TextChannel
import globs 
import module

class EconomyModule(module.Module):
    """Handles generic economy based commands and economy data updates"""
    def __init__(self):
        super().__init__()
        globs.cursor.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT PRIMARY KEY, balance NUMERIC(32, 2));")
        globs.cursor.execute("SELECT * FROM economy;")
        self.data_table = globs.cursor.fetchall()
        self.data: dict[int, float] = {user_id: user_balance for user_id, user_balance in self.data_table}
    STARTING_BALANCE = 100000

    def refresh_data(self) -> None:
        globs.cursor.execute("SELECT * FROM economy;")
        self.data_table = globs.cursor.fetchall()
        self.data = {user_id: user_balance for user_id, user_balance in self.data_table}

    def get_balance(self, userid: int) -> float:
        self.refresh_data()
        return self.data.get(userid, 0)

    def update_balance(self, userid: int, amount: float) -> None:
        globs.cursor.execute("INSERT INTO economy (userid, balance) VALUES (%s, %s) ON CONFLICT (userid) DO UPDATE SET balance = EXCLUDED.balance;", (userid, amount))
        globs.connection.commit()
        self.refresh_data()

    async def get_res(self, msg:Message) -> str:
        class CommandTypes(Enum):
            BALANCE = "balance"
        user_id = msg.author.id
        valid_commands = {member.value for member in CommandTypes}
        msg_set = set(msg.content.lower().split())
        if "!economy" not in msg.content.lower() or valid_commands.isdisjoint(msg_set):
            return
        if CommandTypes.BALANCE.value in msg_set:
            user_balance = self.get_balance(user_id)
            return f"Balance: {user_balance}"
        return