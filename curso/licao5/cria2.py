try:
    arq=open('novo2.txt','x')
    try:
        arq.write('Minha terra tem palmeiras\n')
        arq.write('Onde canta o sabiá\n')
        arq.write('As aves que aqui gorjeiam\n')
        print('Não gorjeiam como lá',file=arq)
        arq.close()
    finally:
        arq.close()
except FileExistsError:
    print('O arquivo "novo2.txt" já existe!')
