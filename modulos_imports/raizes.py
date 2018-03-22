import cdelta
import math
def calcRaizes(a,b,c):
    delta = cdelta.calcDelta(a,b,c)
    if math.isnan(delta):
        print('Não possui raízes reais')
    elif delta == 0:
        raiz = -b / 2*a
        print('Possui apenas uma raiz: ',raiz)
    else:
        x1 = (-b + math.sqrt(delta)) / 2*a
        x2 = (-b - math.sqrt(delta)) / 2*a
        print('X1: ',x1,', X2: ',x2)