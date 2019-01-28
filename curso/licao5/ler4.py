try:
    with open('novo3.txt') as texto:
        linha = texto.readline()
        i = 0
        while linha:
            i+=1
            print('Linha: {}: {}'.format(i,linha.strip()))
            linha = texto.readline()
        print('Eu li {} linhas'.format(i))
except FileNotFoundError:
    print('O arquivo não existe!')