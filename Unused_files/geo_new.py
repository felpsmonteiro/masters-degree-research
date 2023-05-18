import numpy as np
import functions as fc

import mechanisms

a = [60, 30, 9, 1]

b = mechanisms.geometric(a, .1)

printnp.sum(b)