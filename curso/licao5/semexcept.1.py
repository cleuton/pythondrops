try:
    a=open('arquivo.txt')
    print(a.read())
except:
    print('Arquivo inexistente')