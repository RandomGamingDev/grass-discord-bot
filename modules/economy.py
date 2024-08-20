import globs 

class EconomyModule(): 
    def __init__(self): 
        globs.cursor.execute("CREATE TABLE IF NOT EXISTS economy (userid BIGINT PRIMARY KEY, balance NUMERIC(32, 2));")
        globs.cursor.execute("SELECT * FROM economy;") 
        data_table = globs.cursor.fetchall()
        self.data: dict[int, float] = {user_id: user_balance for user_id, user_balance in data_table} 

    def get_balance(self, userid: int) -> float: 
        return self.data.get(userid, 0) 

    def update_balance(self, userid: int, amount: float) -> None: 
            globs.cursor.execute("INSERT INTO economy (userid, balance) VALUES (%s, %s) ON CONFLICT (userid) DO UPDATE SET balance = EXCLUDED.balance;", (userid, amount))
            globs.connection.commit()

    STARTING_BALANCE = 100000  
