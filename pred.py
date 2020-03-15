import numpy as np


def daily(n, growth_factor, days):
    neo_n = []
    curr = n[-1]
    for i in range(days):
        curr *= np.mean(growth_factor)
        neo_n.append(curr)
    return neo_n


def prophet(n, daily_growth):
    neo_n = []
    curr = n[-1]
    n = n[:len(daily_growth)]
    for i in range(len(n)):
        curr = curr + daily_growth[i]
        neo_n.append(curr)
    return neo_n
