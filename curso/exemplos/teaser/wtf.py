achou = False
def procura(t):
    posic = -1
    for i,z in enumerate(t):
        if z=='*':
            achou = True
            posic = i
            break
    return posic

texto = input('Informe um texto: ')
print('Texto digitado: ' + texto)
p = procura(texto)
if achou:
    print('Achou na posição: ',p)
else:
    print('Não achou!')
