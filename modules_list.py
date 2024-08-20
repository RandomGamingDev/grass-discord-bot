from typing import List

import module
from modules import counter, ping, randchoice, roulette, economy

modules: List[module.Module] = [
    ping.PingModule(),
    economy.EconomyModule(),
    roulette.RouletteModule(),
    counter.CounterModule(),
    randchoice.RandomModule(),
]
