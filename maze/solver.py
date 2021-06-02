from model.stack import Stack
from model import constantes

class Solver:

    def __init__(self):
        self._pilha = Stack() 
        self._corrente = None
        self._caminho = []
        # Norte, Sul, Leste, Oeste:
        self._incrementos = [
            [0,-1],[0,1],[1,0],[-1,0]
        ]
        self._visitadas = []
        self._plabirinto = None

    def solve(self,labirinto):
        for xLin in range(labirinto.linhas):
            colunas = []
            for xCol in range(labirinto.colunas):
                colunas.append(False);
            self._visitadas.append(colunas)
        self._plabirinto = labirinto
        self._corrente = labirinto.celulas[0][0]
        self._pilha.push(self._corrente)
        self.procurar()
        while(self._pilha.top):
            self._caminho.append(self._pilha.pop())
        labirinto.caminho = self._caminho

    def procurar(self):
        buffer = None
        while(self._pilha.top):
            self._visitadas[self._corrente.y][self._corrente.x]=True
            if self._corrente.fim:
                return
            proxima = None
            for parede in range(4):
                if not self._corrente.paredes[parede]:
                    if parede == constantes.NORTE and self._corrente.y == 0:
                        continue
                    coluna = self._corrente.x + self._incrementos[parede][0]
                    linha = self._corrente.y + self._incrementos[parede][1]
                    if coluna >= self._plabirinto.colunas or \
                        linha >= self._plabirinto.linhas:
                        continue
                    if self._visitadas[linha][coluna]:
                        continue
                    proxima = self._plabirinto.celulas[linha][coluna]
                    if buffer:
                        self._pilha.push(buffer)
                        buffer = None
                    self._pilha.push(proxima)
                    self._corrente = proxima
                    break
            if not proxima:
                self._corrente = self._pilha.pop()
                buffer = self._corrente

    
