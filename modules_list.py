from typing import List

import module
from modules import counter, ping

modules: List[module.Module] = [
    ping.PingModule(),
    counter.CounterModule(),
]
