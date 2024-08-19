import globs 

class EconomyModule(): 
    def __init__(self): 
        globs.cursor.execute(f"CREATE TABLE IF NOT EXISTS economy (userid BIGINT PRIMARY KEY, balance BIGINT);")
        globs.cursor.execute(f"SELECT * FROM economy;") 
        data_table = globs.cursor.fetchall()
        self.data = {user_id: user_balance for user_id, user_balance in data_table} 

    def get_balance(self, userid): 
        return self.data.get(userid, 0) 

    def update_balance(self, userid, amount): 
            globs.cursor.execute(f"INSERT INTO economy (userid, balance) VALUES (%s, %s) ON CONFLICT (userid) DO UPDATE SET balance = EXCLUDED.balance;", (userid, amount))
            globs.connection.commit()

    STARTING_BALANCE = 100000  