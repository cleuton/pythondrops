import sys
try:
    a=open('arquivo.txt')
    print(a.read())
except FileNotFoundError:
    print('Arquivo inexistente')
except:
    print('Erro inesperado: {}'.format(sys.exc_info()[0]))
    raise
else:
    print('não deu erro')
finally:
    print('com erro ou sem erro, eu sempre executarei!')