import module
from discord import Intents, Client, Message, TextChannel
import globs
import re 
import random
from enum import Enum



class RouletteModule(module.Module): 
    def __init__(self):
        super().__init__()

        globs.cursor.execute("CREATE TABLE IF NOT EXISTS money (userid bigint PRIMARY KEY, balance bigint);")
        
        globs.cursor.execute("SELECT * FROM money;") 
        data_table = globs.cursor.fetchall() 
        self.user_balances = {user_id: user_balance for user_id, user_balance in data_table} 
        self.deltaMoney = 0 
    
    async def get_res (self, msg: Message): 
        if "!roulette" not in msg.lower(): 
            return
        
        if usr_msg.author.id not in self.user_balances: 
            self.user_balances[usr_msg.author.id] = 1000 
        
        class BetTypes(Enum):
            STRAIGHT = "straight" 
            SPLIT = "split"
            STREET = "street"
            CORNER = "corner"
            SIXLINE = "sixline"
            REDBLACK = "redblack" ## Obligatory 34 joke
            DOZEN = "dozen"
            COLUMN = "column"
            ODDEVEN = "oddeven"
            HIGHLOW = "highlow"  
        class BetCalls(Enum): 
            RED = "red"
            BLACK = "black" 
            COLUMN1 = "column1"
            COLUMN2 =  "column2"
            COLUMN3 = "column3"
            DOZEN1 = "first" 
            DOZEN2 = "second"
            DOZEN3 = "third" 
            EVEN = "even"
            ODD = "odd" 
            HIGH = "high"
            LOW = "low"
        class Error(Enum): 
            ERROR = "ERROR" 
        
        player_balance = self.user_balances[usr_msg.author.id]  
        
        def parse_bet(message):
        ## Get information about bet type, player call, and wager while also checking to make sure that the values won't break the roulette wheel.      
            valid_types =  {"straight", "split", "street", "corner", "sixline", "redblack", "dozen", "column", "oddeven", "highlow"}  
            valid_calls =  {"red", "black", "column1", "column2", "column3", "first", "second", "third", "even", "odd", "high", "low"} 
            unpacked_bet = message.lower.split()
            bet_type = unpacked_bet[1] 
            if bet_type not in valid_types: bet_type = Error.ERROR.value  
            player_bet = unpacked_bet[2].split(",")
            for i in range(len(player_bet)):  
                if player_bet[i] == "00": player_bet[i] = -1 
                else:
                    try: 
                        player_bet[i] = int(player_bet[i]) 
                        if player_bet[i] < -1 or player_bet[i] > 36: player_bet[i] = Error.ERROR.value  
                    except ValueError:
                        if player_bet[i] not in valid_calls: player_bet[i] = Error.ERROR.value 
                        else: pass  
            try: 
                wager = int(unpacked_bet[3])
                if wager > player_balance or wager < 0: wager = Error.ERROR.value
            except ValueError: wager = Error.ERROR.value 
            return bet_type, player_bet, wager     

        def is_adjacent(numbers): 
            return all(abs(numbers[i] - numbers[i+1]) == 1 for i in range(len(numbers) - 1)) 

        def roulette(player_bet_statement):
            bet_type, player_bet, wager = parse_bet(player_bet_statement)
            ## Checking for errors returned by parse_bet(message) to see if the roulette should abort or continue  
            if wager == Error.ERROR.value or Error.ERROR.value in player_bet or bet_type == Error.ERROR.value: return Error.ERROR.value, None     
            player_bet_frozenset = frozenset(player_bet) 

            ## Building the roulette table and valid plays for streets, splits, and sixlines 
            RED_NUMS = {number for number in {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}} 
            BLACK_NUMS = {number for number in {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}} 
            COLUMN_1_NUMS = {(1 + 3*i) for i in range (12)} 
            COLUMN_2_NUMS = {(2 + 3*i) for i in range (12)} 
            COLUMN_3_NUMS = {(3 + 3*i) for i in range (12)}
            DOZEN_1_NUMS = {i for i in range(1,12)} 
            DOZEN_2_NUMS = {i for i in range (13,24)} 
            DOZEN_3_NUMS = {i for i in range (25,36)}   
            VALID_STREETS = {frozenset({i, i+1, i+2}) for i in range (1,34,3)} 
            VALID_SIXLINES = {frozenset({i, i+1, i+2, i+3, i+4, i+5}) for i in range (1,31,3)}
            VALID_SPLITS = {frozenset({i, i+1}) for i in range(1, 36)} | {frozenset({i, -1}) for i in range(1, 37)}
            
            ## Creates int_spin_result for checking against and str_spin_result for printing the result into the Discord channel 
            int_spin_result = random.randint(-1,36) 
            if int_spin_result != -1: str_spin_result = str(int_spin_result) 
            elif int_spin_result == -1: str_spin_result = "00" 

            ## Checks for presence of the result within a player's numerical bet 
            def result_match(player_bet_frozenset, int_spin_result): 
                return int_spin_result in player_bet_frozenset

            loss_value = wager * -1 

            ## Handling for each bet type 
            match bet_type: 
                case BetTypes.STRAIGHT.value: 
                    if int_spin_result in player_bet: winnings = wager * 34 
                    else: winnings = loss_value
                case BetTypes.SPLIT.value: 
                    if len(player_bet) != 2 or player_bet_frozenset not in VALID_SPLITS: winnings = Error.ERROR.value
                    elif result_match(player_bet_frozenset, int_spin_result) == False: winnings = loss_value   
                    else: winnings = wager * 16 
                case BetTypes.STREET.value: 
                    if len(player_bet) != 3 or player_bet_frozenset not in VALID_STREETS: winnings = Error.ERROR.value
                    elif result_match(player_bet_frozenset, int_spin_result) == False: winnings = loss_value     
                    else: winnings = wager * 10 
                case BetTypes.CORNER.value: 
                    if len(player_bet) != 4 or is_adjacent(player_bet) == False: winnings = Error.ERROR.value 
                    elif result_match(player_bet_frozenset, int_spin_result) == False: winnings = loss_value   
                    else: winnings = wager * 7 
                case BetTypes.SIXLINE.value: 
                    if len(player_bet) != 6 or player_bet_frozenset not in VALID_SIXLINES: winnings = Error.ERROR.value
                    elif result_match(player_bet_frozenset, int_spin_result) == False: winnings = loss_value    
                    else: winnings = wager * 4 
                case BetTypes.REDBLACK.value: ##Obligatory 34 joke 
                    if int_spin_result in RED_NUMS and player_bet[0] == BetCalls.RED.value: winnings = wager 
                    elif int_spin_result in BLACK_NUMS and player_bet[0] == BetCalls.BLACK.value: winnings = wager 
                    else: winnings = 0 
                case BetTypes.DOZEN.value:
                    if int_spin_result in DOZEN_1_NUMS and player_bet[0] == BetCalls.DOZEN1.value: winnings = wager  
                    elif int_spin_result in DOZEN_2_NUMS and player_bet[0] == BetCalls.DOZEN2.value: winnings = wager  
                    elif int_spin_result in DOZEN_3_NUMS and player_bet[0] == BetCalls.DOZEN3.value: winnings = wager  
                    else: winnings = loss_value 
                case BetTypes.COLUMN.value:
                    if int_spin_result in COLUMN_1_NUMS and player_bet[0] == BetCalls.COLUMN1.value: winnings = wager  
                    elif int_spin_result in COLUMN_2_NUMS and player_bet[0] == BetCalls.COLUMN2.value: winnings = wager 
                    elif int_spin_result in COLUMN_3_NUMS and player_bet[0] == BetCalls.COLUMN3.value: winnings = wager 
                    else: winnings = loss_value 
                case BetTypes.ODDEVEN.value: 
                    if int_spin_result in range(1,36) and int_spin_result % 2 == 0 and player_bet[0] == BetCalls.EVEN.value: winnings = wager
                    elif int_spin_result in range(1,36) and int_spin_result % 2 != 0 and player_bet[0] == BetCalls.ODD.value: winnings = wager
                    else: winnings = loss_value
                case BetTypes.HIGHLOW.value: 
                    if int_spin_result in range(1,18) and player_bet[0] == BetCalls.LOW.value: winnings = wager
                    elif int_spin_result in range(19,36) and player_bet[0] == BetCalls.HIGH.value: winnings = wager
                    else: winnings = loss_value 
            return str_spin_result, winnings 
        str_spin_result, winnings = roulette()
        ## Checks if roulette threw an error, if not continues with updating information and printing result to Discord channel 
        if str_spin_result == Error.ERROR.value or winnings == Error.ERROR.value: return f"lmfao"
        else: 
            self.deltaMoney = winnings     
            return f"The roulette wheel landed on {str_spin_result}, giving you a profit of {winnings}"
        
        roulette(msg.content) 
    
    async def after_res(self): 
        updatedBalance = self.user_balances[usr_msg_author_id] + self.deltaMoney  
        globs.cursor.execute(f"UPDATE money SET balance=%s WHERE userid=%s;", updatedBalance, usr_msg_author_id) 


