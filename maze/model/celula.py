class Celula():
    def __init__(self):
        self.paredes = [True, True, True, True];
        self.visitada = False;
        self.inicio = False;
        self.fim = False;
        self.x = 0;
        self.y = 0;
        self.ocupada = False;
        self.objeto = 0;        