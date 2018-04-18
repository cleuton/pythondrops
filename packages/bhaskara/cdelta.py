def calcDelta(a,b,c):
    delta = b**2 - 4*a*c
    if delta < 0:
        return float('nan')
    else:
        return delta