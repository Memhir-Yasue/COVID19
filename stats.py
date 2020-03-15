def get_growth_factor(n):
    growth_factor = []
    for i in range(1, len(n)):
        growth_factor.append(n[i]/n[i-1])
    return growth_factor