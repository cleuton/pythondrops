import sys
from util.primo import crivo

def calcular(numero,sinal_ultimo):
    resultado=[]
    valor=numero
    lprimos=crivo(numero)
    i=0
    primo=lprimos[i]
    while valor > 1:
        resto=valor%primo
        if resto > 0:
            i=i+1
            primo = lprimos[i]
        else:
            valor = valor / primo
            if valor==1:
                primo = primo * sinal_ultimo
            resultado.append(primo)   
    return resultado

if __name__=='__main__':
    numero=int(sys.argv[1])
    resultado = None
    if numero==0:
        resultado=[0]
    else:
        if numero > 0 and numero < 3:
            resultado = [numero]
        else:
            valor = numero
            sinal=1
            if numero < 0:
                sinal=-1
                valor=numero * (-1)
            resultado = calcular(valor,sinal)
    print(resultado)    
