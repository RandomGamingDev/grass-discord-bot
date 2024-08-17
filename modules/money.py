import globs 

class MoneyModule(): 
    def __init__(self): 
        globs.cursor.execute("CREATE TABLE IF NOT EXISTS money (userid bigint PRIMARY KEY, balance bigint);")
        globs.cursor.execute("SELECT * FROM money") 
        data_table = globs.cursor.fetchall() 
        self.data = {user_id: user_balance for user_id, user_balance in data_table} 

    def get_balance(self, userid): 
        return self.data.get(userid, 0) 

    def update_balance(self, userid, amount): 
            globs.cursor.execute("INSERT INTO money (userid, balance) VALUES (%s, %s) ON CONFLICT (userid) DO UPDATE SET balance = EXCLUDED.balance", (userid, amount))   