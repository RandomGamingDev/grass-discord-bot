import typing
import random
from enum import Enum
import globs
from discord import Intents, Client, Message, TextChannel
from shared.economydata import EconomyInstance
import module

class RouletteModule(module.Module):
    """Runs roulette module, returns roulette spin result and profit"""
    def __init__(self):
        super().__init__()
        self.profit = 0
        self.result = ""
        self.user_id = 0
        self.player_balance = 0

    async def get_res(self, msg:Message) -> str:
        """Checks Discord message and takes control if applicable, running the roulette game"""
        if "!roulette" not in msg.content.lower():
            return
        class BetTypes(Enum):
            """All of the valid bet types in American roulette, barring special bets"""
            STRAIGHT = "straight"
            SPLIT = "split"
            STREET = "street"
            CORNER = "corner"
            SIXLINE = "sixline"
            REDBLACK = "redblack"
            DOZEN = "dozen"
            COLUMN = "column"
            ODDEVEN = "oddeven"
            HIGHLOW = "highlow"
        class BetCalls(Enum):
            """All of the valid player calls in American roulette, barring special calls"""
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
        class Bet():
            """Object to contain player bet information from parse_bet()"""
            def __init__(self, bet_type, player_bet, wager):
                self.bet_type = bet_type
                self.player_bet = player_bet
                self.wager = wager
        temp_id = msg.author.id
        temp_balance = EconomyInstance.get_balance(temp_id)
        ## Force refresh of balance and id
        self.player_balance = temp_balance
        self.user_id = temp_id
        def parse_bet(message: str) -> Bet:
            """Retrieves player bet type, player bet call, and player's wager to store in a Bet object"""
            unpacked_bet = message.lower().split()
            valid_types = {member.value for member in BetTypes}
            valid_calls = {member.value for member in BetCalls}
            bet_type = unpacked_bet[1]
            if bet_type not in valid_types:
                raise ValueError
            player_bet = unpacked_bet[2].split(",")
            for i, sub_bet in enumerate(player_bet):
                if sub_bet == "00":
                    player_bet[i] = -1
                else:
                    try:
                        player_bet[i] = int(sub_bet)
                        if player_bet[i] < -1 or player_bet[i] > 36:
                            raise ValueError
                    except ValueError:
                        if sub_bet not in valid_calls:
                            raise ValueError
            wager = int(unpacked_bet[3])
            if wager > self.player_balance or wager < 0:
                raise ValueError
            bet = Bet(bet_type, player_bet, wager)
            return bet
        def is_adjacent(numbers) -> bool:
            """Checks to see if the player's bet contains subsequent numbers for a corner bet"""
            return all(abs(numbers[i] - numbers[i+1]) == 1 for i in range(len(numbers) - 1))
        def roulette(player_bet_statement) -> None:
            """Simulates the roulette game, returns result and profit"""
            ## Validation of player's bet statement
            bet = parse_bet(player_bet_statement)
            player_bet_frozenset = frozenset(bet.player_bet)

            ## Creation of roulette board
            red_nums = {number for number in {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}}
            black_nums = {number for number in {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}}
            column_1_nums = {(1 + 3*i) for i in range (12)}
            column_2_nums = {(2 + 3*i) for i in range (12)}
            column_3_nums = {(3 + 3*i) for i in range (12)}
            dozen_1_nums = {i for i in range(1,13)}
            dozen_2_nums = {i for i in range (13,25)}
            dozen_3_nums = {i for i in range (25,37)}
            valid_streets = {frozenset({i, i+1, i+2}) for i in range (1,34,3)}
            valid_sixlines = {frozenset({i, i+1, i+2, i+3, i+4, i+5}) for i in range (1,31,3)}
            valid_splits = {frozenset({i, i+1}) for i in range(-1, 36)}

            ## Spins random number- int_spin_result for checking against and str_spin_result for printing
            int_spin_result = random.randint(-1,36)
            if int_spin_result != -1:
                self.result = str(int_spin_result)
            elif int_spin_result == -1:
                self.result = "00"

            def result_match(player_bet_frozenset, int_spin_result) -> bool:
                """Checks for presence of the result within a player's numerical bet"""
                return int_spin_result in player_bet_frozenset

            loss_value = -bet.wager

            ## Handling for each bet type
            if bet.bet_type == BetTypes.STRAIGHT.value:
                if len(bet.player_bet) != 1:
                    raise ValueError
                elif int_spin_result in bet.player_bet:
                    self.profit = bet.wager * 34
                else: self.profit = loss_value
            elif bet.bet_type == BetTypes.SPLIT.value:
                if len(bet.player_bet) != 2 or player_bet_frozenset not in valid_splits:
                    raise ValueError
                elif not result_match(player_bet_frozenset, int_spin_result):
                    self.profit = loss_value
                else: self.profit = bet.wager * 16
            elif bet.bet_type == BetTypes.STREET.value:
                if len(bet.player_bet) != 3 or player_bet_frozenset not in valid_streets:
                    raise ValueError
                elif not result_match(player_bet_frozenset, int_spin_result):
                    self.profit = loss_value
                else: self.profit = bet.wager * 10
            elif bet.bet_type == BetTypes.CORNER.value:
                if len(bet.player_bet) != 4 or not is_adjacent(bet.player_bet):
                    raise ValueError
                elif not result_match(player_bet_frozenset, int_spin_result):
                    self.profit = loss_value
                else: self.profit = bet.wager * 7
            elif bet.bet_type == BetTypes.SIXLINE.value:
                if len(bet.player_bet) != 6 or player_bet_frozenset not in valid_sixlines:
                    raise ValueError
                elif not result_match(player_bet_frozenset, int_spin_result):
                    self.profit = loss_value
                else: self.profit = bet.wager * 4
            elif bet.bet_type == BetTypes.REDBLACK.value:
                if int_spin_result in red_nums and bet.player_bet[0] == BetCalls.RED.value:
                    self.profit = bet.wager
                elif int_spin_result in black_nums and bet.player_bet[0] == BetCalls.BLACK.value:
                    self.profit = bet.wager
                else: self.profit = loss_value
            elif bet.bet_type == BetTypes.DOZEN.value:
                if int_spin_result in dozen_1_nums and bet.player_bet[0] == BetCalls.DOZEN1.value:
                    self.profit = bet.wager
                elif int_spin_result in dozen_2_nums and bet.player_bet[0] == BetCalls.DOZEN2.value:
                    self.profit = bet.wager
                elif int_spin_result in dozen_3_nums and bet.player_bet[0] == BetCalls.DOZEN3.value:
                    self.profit = bet.wager
                else: self.profit = loss_value
            elif bet.bet_type == BetTypes.COLUMN.value:
                if int_spin_result in column_1_nums and bet.player_bet[0] == BetCalls.COLUMN1.value:
                    self.profit = bet.wager
                elif int_spin_result in column_2_nums and bet.player_bet[0] == BetCalls.COLUMN2.value:
                    self.profit = bet.wager
                elif int_spin_result in column_3_nums and bet.player_bet[0] == BetCalls.COLUMN3.value:
                    self.profit = bet.wager
                else: self.profit = loss_value
            elif bet.bet_type == BetTypes.ODDEVEN.value:
                if int_spin_result in range (1,37) and int_spin_result % 2 == 0 and bet.player_bet[0] == BetCalls.EVEN.value:
                    self.profit = bet.wager
                elif int_spin_result in range (1,37) and int_spin_result %2 != 0 and bet.player_bet[0] == BetCalls.ODD.value:
                    self.profit = bet.wager
                else: self.profit = loss_value
            elif bet.bet_type == BetTypes.HIGHLOW.value:
                if int_spin_result in range(1,19) and bet.player_bet[0] == BetCalls.LOW.value:
                    self.profit = bet.wager
                if int_spin_result in range(19,37) and bet.player_bet[0] == BetCalls.HIGH.value:
                    self.profit = bet.wager
                else: self.profit = loss_value
            return
        ## Runs and checks if roulette threw an error, if not updates database and prints message
        try:
            roulette(msg.content)
            return f"The Roulette wheel landed on {self.result}, giving you a profit of {self.profit}"
        except ValueError:
            self.profit = ""
            return "lmfao"

    async def after_res(self, usr_msg=Message, bot_msg=Message) -> None:
        """Updates database if result was valid"""
        if isinstance(self.profit, int):
            updated_balance = self.player_balance + self.profit
            EconomyInstance.update_balance(self.user_id, updated_balance)
        else: return
