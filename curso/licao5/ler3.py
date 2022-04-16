try:
    with open('novo3.txt') as texto:
        for linha in texto:
            print(linha.strip())
except FileNotFoundError:
    print('O arquivo não existe!')