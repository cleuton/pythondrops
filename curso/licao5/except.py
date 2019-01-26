import sys
def fn1():
    raise ValueError('Ferrou')

def fn2():
    try:
        print('comando1')
        fn1()
        print('outro comando')
    except OSError as oserro:
        print("Erro do Sistema Operacional: {0}".format(oserro))

try:
    fn2()
except ValueError as erro:
    print('Value Error: {}'.format(erro))
except:
    print('ERRO:', sys.exc_info()[0])
    raise