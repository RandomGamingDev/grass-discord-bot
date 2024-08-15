from typing import Final, Tuple
import sys
import module
sys.path.insert(1, "modules")

import ping
import counter
modules: Tuple[module.Module] = (
	ping.PingModule(),
	counter.CounterModule(),
)