try:
    with open('novo3.txt','x') as arq:
        arq.write('Minha terra tem palmeiras\n')
        arq.write('Onde canta o sabiá\n')
        arq.write('As aves que aqui gorjeiam\n')
        print('Não gorjeiam como lá',file=arq)
except FileExistsError:
    print('O arquivo já existe!')