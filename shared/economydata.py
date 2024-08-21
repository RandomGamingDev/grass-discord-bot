import typing
import globs

class EconomyData():
    """Handles connection and updates to economy data table"""
    def __init__(self):
        globs.cursor.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT PRIMARY KEY, balance NUMERIC(32, 2));")
        globs.cursor.execute("SELECT * FROM economy;")
        self.data_table = globs.cursor.fetchall()
        self.data_dict: [int, float] = {user_id: user_balance for user_id, user_balance in self.data_table}
        self.STARTING_BALANCE = 100000

    def refresh_data(self) -> None:
        globs.cursor.execute("SELECT * FROM economy;")
        self.data_table = globs.cursor.fetchall()
        self.data_dict = {user_id: user_balance for user_id, user_balance in self.data_table}

    def get_balance(self, user_id: int) -> float:
        self.refresh_data()
        if user_id not in self.data_dict:
            self.update_balance(user_id, self.STARTING_BALANCE)
        return self.data_dict.get(user_id)

    def update_balance(self, user_id: int, amount:float) -> None: 
        globs.cursor.execute("INSERT INTO economy (userid, balance) VALUES (%s, %s) ON CONFLICT (userid) DO UPDATE SET balance = EXCLUDED.balance;", (user_id, amount))
        globs.connection.commit()
        self.refresh_data()
EconomyInstance = EconomyData()
