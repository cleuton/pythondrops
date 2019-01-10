LARGURA=1000
ALTURA=1000
GABARITO_OBJETO={'x1':0,'y1':0,'x2':5,'y2':5}
DIRECAO={'cima':(0,+1),'baixo':(0,-1),'esq':(-1,0),'dir':(+1,0)}
objetos=[]

def colisao(objeto1,objeto2):
    if objeto1['x1']> objeto2['x2']or objeto2['x1']> objeto1['x2']:
        return False
    if objeto1['y1'] < objeto2['y2'] or objeto2['y1'] < objeto1['y2']: 
        return False
    return True

def mover(objeto,direcao):
    novo=GABARITO_OBJETO.copy()
    novo['x1']=objeto['x1']+DIRECAO[direcao][0]
    novo['y1']=objeto['y1']+DIRECAO[direcao][1]
    novo['x2']=objeto['x2']+DIRECAO[direcao][0]
    novo['y2']=objeto['y2']+DIRECAO[direcao][1]   
    if novo['x1']<0 or novo['x2']==LARGURA:
        return False
    if novo['y1']==ALTURA or novo['y2']<0:
        return False
    objeto['x1']=novo['x1']
    objeto['y1']=novo['y1']
    objeto['x2']=novo['x2']
    objeto['y2']=novo['y2']   
    return True

if __name__=='__main__':
    print(__name__)
    objeto1=GABARITO_OBJETO.copy()
    objeto2=GABARITO_OBJETO.copy()
    objeto3=GABARITO_OBJETO.copy()

    objeto1['x1']=0
    objeto1['y1']=10
    objeto1['x2']=10
    objeto1['y2']=0

    objeto2['x1']=5
    objeto2['y1']=5
    objeto2['x2']=15
    objeto2['y2']=0

    objeto3['x1']=15
    objeto3['y1']=15
    objeto3['x2']=20
    objeto3['y2']=10

    print(colisao(objeto1,objeto2))
    print(colisao(objeto1,objeto3))
    retorno=mover(objeto1,'dir')
    if retorno:
        print('Moveu objeto1 para a direita: ',objeto1)
    retorno=mover(objeto3,'cima')
    if retorno:
        print('Moveu objeto3 para cima: ',objeto3)
    retorno=mover(objeto3,'esq')
    if retorno:
        print('Moveu objeto3 para esquerda: ',objeto3)
    retorno=mover(objeto3,'baixo')
    if retorno:
        print('Moveu objeto3 para baixo: ',objeto3)    
    objeto4=GABARITO_OBJETO.copy()
    objeto4['x1']=LARGURA-11
    objeto4['y1']=ALTURA-1
    objeto4['x2']=LARGURA-1
    objeto4['y2']=ALTURA-11
    retorno=mover(objeto4,'dir')
    if not retorno:
        print('Não pode mover para a direita: ',objeto4) 
    retorno=mover(objeto4,'cima')
    if not retorno:
        print('Não pode mover para cima: ',objeto4)  
    retorno=mover(objeto1,'esq')
    retorno=mover(objeto1,'esq')
    if not retorno:
        print('Não pode mover para a esquerda: ',objeto1)   
    retorno=mover(objeto1,'baixo')
    if not retorno:
        print('Não pode mover para baixo: ',objeto1) 