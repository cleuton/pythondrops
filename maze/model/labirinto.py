from model.celula import Celula
from model.stack import Stack
from model import constantes
from random import randint
from termcolor import colored

class Labirinto:
    
    def __init__(self,linhas=10,colunas=10):
        self.linhas = linhas
        self.colunas = colunas
        self.celulas = []
        self.celulaInicial = None
        self.celunaFinal = None
        self.valido = False
        self._corrente = None
        self._proxima = None
        self._qtdTotal = 0
        self._qtdVisitadas = 0
        self._pilha = Stack()       
        self.inicializar()
        self.caminho = None

    def inicializar(self):
        contador = 0
        while contador < 4:
            self.celulas=[]
            for i in range(self.linhas):
                linha = []
                for j in range(self.colunas):
                    celula = Celula()
                    celula.y=i
                    celula.x=j
                    celula.inicio=False
                    celula.fim=False
                    celula.visitada=False
                    linha.append(celula)
                self.celulas.append(linha)
            self.celulas[0][0].inicio = True
            self.celulas[-1][-1].fim = True
            contador = contador + 1
            self.pilha = Stack()
            self._qtdVisitadas = 0
            self.criar()
            if (not self.fechada(self.celulas[1][1])) and \
                (not self.fechada(self.celulas[-2][-2])):
                break
        if contador<4:
            self.valido=True

    def fechada(self,celula):
        retorno=False
        if celula.paredes[constantes.NORTE] and \
            celula.paredes[constantes.SUL] and \
            celula.paredes[constantes.LESTE] and \
            celula.paredes[constantes.OESTE]:
            retorno = True
        return retorno

    def criar(self):
        self._qtdTotal = self.linhas * self.colunas
        linha = randint(0,self.linhas - 1)
        coluna = randint(0,self.colunas - 1)
        self._corrente = self.celulas[linha][coluna]
        self._corrente.visitada = True
        self._proxima = self.pegarVizinha(self._corrente)
        self._proxima.visitada = True
        self.quebrarParedes(self._corrente, self._proxima)
        self.pilha.push(self._corrente)
        self._qtdVisitadas=self._qtdVisitadas - 1
        self._corrente = self._proxima
        self.processaCelula()        

    def processaCelula(self):
        while True:
            if self.pilha.top:
                if self.isDeadEnd(self._corrente) or \
                    self._corrente.fim or \
                    self._corrente.inicio:
                    self._proxima = self.pilha.pop()
                    self._corrente = self._proxima
                else:
                    self._proxima = self.pegarVizinha(self._corrente)
                    self.quebrarParedes(self._corrente,self._proxima)
                    self.pilha.push(self._corrente)
                    self._proxima.visitada = True
                    self._qtdVisitadas = self._qtdVisitadas + 1
                    self._corrente = self._proxima
            else:
                self.celulas[0][0].paredes[constantes.NORTE]=False
                self.celulas[-1][-1].paredes[constantes.SUL]=False
                return
    
    def isDeadEnd(self,celula):
        if celula.y:
            if not self.celulas[(celula.y-1)][celula.x].visitada:
                return False
        if celula.y < (self.linhas - 1):
            if not self.celulas[(celula.y+1)][celula.x].visitada:
                return False
        if celula.x:
            if not self.celulas[celula.y][(celula.x - 1)].visitada:
                return False
        if celula.x < (self.colunas - 1):
            if not self.celulas[celula.y][(celula.x + 1)].visitada:
                return False
        return True

    def quebrarParedes(self,c1,c2):
        if c1.x > c2.x:
            c1.paredes[constantes.OESTE]=False
            c2.paredes[constantes.LESTE]=False
            return
        if c1.x < c2.x:
            c1.paredes[constantes.LESTE]=False
            c2.paredes[constantes.OESTE]=False
            return
        if c1.y > c2.y:
            c1.paredes[constantes.NORTE]=False
            c2.paredes[constantes.SUL]=False
            return
        if c1.y < c2.y:
            c1.paredes[constantes.SUL]=False
            c2.paredes[constantes.NORTE]=False
            return
    
    def pegarVizinha(self,celula):
        procurar = True
        cel = None
        while procurar:
            vizinha = randint(0,3)
            if vizinha==constantes.NORTE:
                if celula.y>0:
                    cel = self.celulas[(celula.y - 1)][celula.x]
            elif vizinha==constantes.SUL:
                if celula.y < (self.linhas - 1):
                    cel = self.celulas[(celula.y + 1)][celula.x]
            elif vizinha==constantes.LESTE:
                if celula.x < (self.colunas - 1):
                    cel = self.celulas[celula.y][(celula.x + 1)]
            else:
                if celula.x > 0:
                    cel = self.celulas[celula.y][(celula.x - 1)]
            if cel and not cel.visitada:
                procurar = False
        return cel

    def __str__(self):
        linhas = [[' ' for i in range((self.colunas * 3)+1)] for j in range(self.linhas * 3)]
        for z in linhas:
            z[-1]='\n'
        for i in range(self.linhas):
            for j in range(self.colunas):
                matriz = self._get_celula(self.celulas[i][j])
                self._insert(linhas,matriz,i,j)
        flattened = [y for x in linhas for y in x]
        return ''.join(flattened)
    
    def _get_celula(self,cel):
        linha1 = [' ',' ',' ']
        linha2 = [' ',' ',' ']
        linha3 = [' ',' ',' ']
        if cel.paredes[constantes.NORTE]:
            linha1 = ['-','-','-']
        if cel.paredes[constantes.SUL]:
            linha3 = ['-','-','-']
        if cel.paredes[constantes.OESTE]:
            linha1[0] = '+' if linha1[0] == '-' else '|'
            linha2[0] = '|'
            linha3[0] = '+' if linha3[0] == '-' else '|'
        if cel.paredes[constantes.LESTE]:
            linha1[2] = '+' if linha1[2] == '-' else '|'
            linha2[2] = '|'
            linha3[2] = '+' if linha3[2] == '-' else '|'
        if self.caminho:
            if self._in_path(cel.y,cel.x):
                linha2[1] = colored(' ', attrs=['reverse'])
        return [linha1,linha2,linha3]       

    def _insert(self,linhas,matriz,i,j):
        linha = i*2
        coluna = j*2
        for l in range(3):
            for c in range(3):
                linhas[linha+l][coluna+c]=matriz[l][c]

    def _in_path(self,linha,coluna):
        for celula in self.caminho:
            if celula.y == linha and celula.x == coluna:
                return True
        return False

                


