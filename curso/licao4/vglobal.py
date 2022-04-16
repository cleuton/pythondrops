achou=False
def procurar(texto):
    global achou
    for c in texto:
        if c=='*' or c=='&':
            achou=True

procurar('Este * um t&xto legal')
print(achou)