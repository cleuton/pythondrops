expressao = [-5.0,'-',2.0,'*',3.0,'+',14.0,'/',-7.0]

posfixa=[]
pilha=[]
prioridades={'+': 1, '-': 1, '*': 2, '/': 2}

# Conversão para expressão posfixa:

for e in expressao:
    if isinstance(e,(int,float)):
        # Copia para a expressão
        posfixa.append(e)
    else:
        if not len(pilha):
            # Pilha vazia
            pilha.append(e)
        else:
            if not prioridades[pilha[-1]]>prioridades[e]:
                pilha.append(e)
            else:
                while len(pilha):
                    posfixa.append(pilha.pop())
                    if not prioridades[posfixa[-1]]>prioridades[e]:
                        break
                pilha.append(e)
while len(pilha):
    posfixa.append(pilha.pop())
print(posfixa)

# Cálculo de expressão posfixa:

pilha=[]
for x in posfixa:
    if isinstance(x,(int,float)):
        pilha.append(x)
    else:
        while len(pilha):
            op2=pilha.pop()
            op1=pilha.pop()
            pilha.append(eval(str(op1)+x+str(op2)))
            break
print('Resultado: ',pilha.pop())