import coeficientes
from bhaskara import raizes
if __name__ == '__main__':
    a,b,c = coeficientes.obterCoeficientes()
    raizes.calcRaizes(a,b,c)